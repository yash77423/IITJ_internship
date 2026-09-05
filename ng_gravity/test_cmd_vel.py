import subprocess
cmd = """ign topic -t /model/reconfig_drone/cmd_vel -m ignition.msgs.Twist -p 'linear: {x: 0, y: 0, z: 0} angular: {z: 0}'"""
subprocess.run(cmd, shell=True)
