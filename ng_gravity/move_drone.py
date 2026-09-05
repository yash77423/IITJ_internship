import subprocess
import time

# ==============================
# USER INPUT
# ==============================
MODEL_NAME = "reconfig_drone"   # Name of drone model in Gazebo
WORLD_NAME = "narrow_gap"    # Name of world

start = [0, 0, 1]
end   = [3, 3, 3]

steps = 50
delay = 0.1

# ==============================
# FOLD ARM Function
# ==============================

def fold_arm(joint_name, angle):
    cmd = f"""
    ign topic -t /model/{MODEL_NAME}/joint/{joint_name}/0/cmd_pos \
    -m ignition.msgs.Double \
    -p 'data: {angle}'
    """
    subprocess.run(cmd, shell=True)

# ==============================
# INITIAL CONFIGURATION = OPEN
# ==============================

print("Setting initial OPEN configuration 🚀")

# Open all arms FIRST

fold_arm("hinge2", 1.57)
fold_arm("hinge3", 1.57)
fold_arm("hinge4", 1.57)
fold_arm("hinge5", 1.57)

time.sleep(1)

# ==============================
# PATH GENERATION
# ==============================
path = []

for i in range(steps + 1):
    t = i / steps
    x = start[0] + t * (end[0] - start[0])
    y = start[1] + t * (end[1] - start[1])
    z = start[2] + t * (end[2] - start[2])
    path.append((x, y, z))

# ==============================
# ==============================
# MOVE DRONE
# ==============================

def send_ign_cmd_vel(vx, vy, vz):
    cmd = f"""
    ign topic -t /{MODEL_NAME}/cmd_vel \
    -m ignition.msgs.Twist \
    -p 'linear: {{x: {vx}, y: {vy}, z: {vz}}} angular: {{x: 0, y: 0, z: 0}}'
    """
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def send_ign_service(x, y, z):
    cmd = f"""
    ign service -s /world/{WORLD_NAME}/set_pose \
    --reqtype ignition.msgs.Pose \
    --reptype ignition.msgs.Boolean \
    --timeout 2000 \
    --req 'name: "{MODEL_NAME}", position: {{x: {x}, y: {y}, z: {z}}}'
    """
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def enable_drone():
    cmd = f"""
    ign topic -t /{MODEL_NAME}/enable \
    -m ignition.msgs.Boolean \
    -p 'data: true'
    """
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Teleport initially
send_ign_service(start[0], start[1], start[2])

# Enable the drone's velocity controller
enable_drone()

# Hover before moving
for _ in range(20):
    send_ign_cmd_vel(0, 0, 0)
    time.sleep(0.1)

vx = (end[0] - start[0]) / (steps * delay)
vy = (end[1] - start[1]) / (steps * delay)
vz = (end[2] - start[2]) / (steps * delay)

for (x, y, z) in path:
    
    send_ign_cmd_vel(vx, vy, vz)
    time.sleep(delay)

print("Reached Point B ✅")

# ==============================
# STOP & STABILIZE
# ==============================
for _ in range(20):
    send_ign_cmd_vel(0, 0, 0)
    time.sleep(0.1)
    
# ==============================
# RECONFIGURATION, FINAL CONFIGURATION = CLOSE
# ==============================
print("Reconfiguring... 🔧")

# Fold all arms
fold_arm("hinge2", 0)
fold_arm("hinge3", 0)
fold_arm("hinge4", 0)
fold_arm("hinge5", 0)

print("Reconfiguration Done ✅")

time.sleep(1)

