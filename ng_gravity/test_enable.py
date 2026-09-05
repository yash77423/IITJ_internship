import subprocess
cmd = "ign topic -t /model/reconfig_drone/enable -m ignition.msgs.Boolean -p 'data: true'"
subprocess.run(cmd, shell=True)
