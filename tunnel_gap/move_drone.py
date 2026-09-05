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
# MOVE DRONE
# ==============================
for (x, y, z) in path:
    
    cmd = f"""
    ign service -s /world/{WORLD_NAME}/set_pose \
    --reqtype ignition.msgs.Pose \
    --reptype ignition.msgs.Boolean \
    --timeout 2000 \
    --req 'name: "{MODEL_NAME}", position: {{x: {x}, y: {y}, z: {z}}}'
    """

    subprocess.run(cmd, shell=True)
    time.sleep(delay)

print("Reached Point B ✅")

# ==============================
# STOP & STABILIZE
# ==============================
time.sleep(2)   # pause after reaching B
    
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

