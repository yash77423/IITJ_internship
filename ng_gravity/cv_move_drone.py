import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from sensor_msgs.msg import Image
import cv2
import numpy as np
import subprocess
import time

MODEL_NAME = "reconfig_drone"
WORLD_NAME = "narrow_gap"

steps = 150
delay = 0.1
# Moving from before the gap to past the gap
start = [-3, 0, 0.5]
end = [3, 0, 0.5]

def send_ign_service(x, y, z):
    cmd = f"""
    ign service -s /world/{WORLD_NAME}/set_pose \
    --reqtype ignition.msgs.Pose \
    --reptype ignition.msgs.Boolean \
    --timeout 2000 \
    --req 'name: "{MODEL_NAME}", position: {{x: {x}, y: {y}, z: {z}}}'
    """
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def send_ign_cmd_vel(vx, vy, vz):
    cmd = f"""
    ign topic -t /{MODEL_NAME}/cmd_vel \
    -m ignition.msgs.Twist \
    -p 'linear: {{x: {vx}, y: {vy}, z: {vz}}} angular: {{x: 0, y: 0, z: 0}}'
    """
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def enable_drone():
    cmd = f"""
    ign topic -t /{MODEL_NAME}/enable \
    -m ignition.msgs.Boolean \
    -p 'data: true'
    """
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def fold_arm(joint_name, angle):
    cmd = f"""
    ign topic -t /model/{MODEL_NAME}/joint/{joint_name}/0/cmd_pos \
    -m ignition.msgs.Double \
    -p 'data: {angle}'
    """
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def set_configuration_open():
    print("Setting OPEN configuration 🚀")
    fold_arm("hinge2", 1.57)
    fold_arm("hinge3", 1.57)
    fold_arm("hinge4", 1.57)
    fold_arm("hinge5", 1.57)

def set_configuration_closed():
    print("Reconfiguring... 🔧")
    fold_arm("hinge2", 0)
    fold_arm("hinge3", 0)
    fold_arm("hinge4", 0)
    fold_arm("hinge5", 0)
    print("Reconfiguration Done ✅")

class DroneCV(Node):
    def __init__(self):
        super().__init__('drone_cv_node')
        
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        self.subscription = self.create_subscription(
            Image,
            '/camera',
            self.image_callback,
            qos_profile)
        self.gap_width_pixels = None
        # We consider a navigability score threshold. The physical gap is wide, but if CV sees the gap width taking less than e.g. 200 pixels, it's far. 
        # When it approaches, gap width in pixels increases.
        # Actually drone_arm_width is simulated as a threshold. 
        self.navigability_score = 999.0 
        self.current_frame = None

    def image_callback(self, msg):
        try:
            cv_image = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
            # OpenCV expects BGR for imshow, but the sensor is R8G8B8. Convert to BGR for display.
            display_frame = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
            self.current_frame = display_frame
            
            # Use HSV for dynamic lighting robustness
            hsv = cv2.cvtColor(display_frame, cv2.COLOR_BGR2HSV)
            mask1 = cv2.inRange(hsv, np.array([0, 50, 50]), np.array([10, 255, 255]))
            mask2 = cv2.inRange(hsv, np.array([160, 50, 50]), np.array([180, 255, 255]))
            red_mask = cv2.bitwise_or(mask1, mask2)
            contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            valid_contours = [c for c in contours if cv2.contourArea(c) > 500] 
            if len(valid_contours) >= 2:
                sorted_contours = sorted(valid_contours, key=lambda c: cv2.boundingRect(c)[0])
                left_contour = sorted_contours[0]
                right_contour = sorted_contours[-1]
                
                x1, _, w1, _ = cv2.boundingRect(left_contour)
                x2, _, w2, _ = cv2.boundingRect(right_contour)
                
                self.gap_width_pixels = x2 - (x1 + w1)
                
                # Draw visual markers on the frame for the user
                cv2.rectangle(self.current_frame, (x1, 0), (x1+w1, 480), (0, 0, 255), 2)
                cv2.rectangle(self.current_frame, (x2, 0), (x2+w2, 480), (0, 0, 255), 2)
                cv2.putText(self.current_frame, f"Gap: {self.gap_width_pixels}px", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                drone_arm_pixel_width = 250
                self.navigability_score = self.gap_width_pixels / drone_arm_pixel_width

        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

def main():
    rclpy.init()
    node = DroneCV()
    
    # Spawn at start position before opening so it isn't in the middle of walls
    # # send_ign_service(start[0], start[1], start[2])
    time.sleep(1)
    
    # Enable the drone's velocity controller
    enable_drone()
    
    set_configuration_open()
    
    for _ in range(20):
        send_ign_cmd_vel(0, 0, 0)
        time.sleep(0.1)
    
    path = []
    for i in range(steps + 1):
        t = i / steps
        x = start[0] + t * (end[0] - start[0])
        y = start[1] + t * (end[1] - start[1])
        z = start[2] + t * (end[2] - start[2])
        path.append((x, y, z))
        
    reconfigured = False
    reopened = False
    
    vx = (end[0] - start[0]) / (steps * delay)
    vy = (end[1] - start[1]) / (steps * delay)
    vz = (end[2] - start[2]) / (steps * delay)
    
    for (x, y, z) in path:
        # Check for incoming camera frames
        rclpy.spin_once(node, timeout_sec=0.01)
        
        # We now command velocity instead of setting exact pose to use physics
        send_ign_cmd_vel(vx, vy, vz)
        
        # Display the live feed if we have a frame
        if node.current_frame is not None:
            cv2.imshow("Drone CV Camera Feed", node.current_frame)
            cv2.waitKey(1)
        else:
            print("[CV] waiting for camera frames...")
            
        if not reconfigured and node.gap_width_pixels is not None:
            N = node.navigability_score
            print(f"[CV] Gap Width px: {node.gap_width_pixels}, Navigability Score N: {N:.2f}")
            if N < 1.0:
                print(f"🚨 Navigability Score {N:.2f} < 1! Triggering Reconfiguration...")
                set_configuration_closed()
                reconfigured = True

        if reconfigured and not reopened and x > 1.5:
            print("✅ Out of narrow passages! Opening again... 🚀")
            set_configuration_open()
            reopened = True

        time.sleep(delay)
        
    # Stop drone at point B
    for _ in range(10):
        send_ign_cmd_vel(0, 0, 0)
        time.sleep(0.1)
        
    print("Reached Point B ✅")

    # Clean up cleanly to avoid "terminate called without active exception"
    cv2.destroyAllWindows()
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()

if __name__ == '__main__':
    main()
