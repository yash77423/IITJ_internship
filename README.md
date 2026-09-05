# Vision-Triggered Morphological Reconfiguration of a Modular Drone  
### Simulation-Based Research Framework using ROS2, Ignition Gazebo, and OpenCV

This repository contains the work carried out during a **5-month research internship** at  
**Indian Institute of Technology Jodhpur (IIT Jodhpur)**    
from **January 2026 – June 2026**.

## Project Title
**Vision-Triggered Morphological Reconfiguration of a Modular Drone Using a Simulation-Based Framework**

---

# 📌 Project Overview

This project explores a **vision-triggered adaptive drone reconfiguration framework**, where a modular drone changes its morphology dynamically after detecting narrow navigable gaps in the environment using computer vision techniques.

The work was implemented primarily using:

- ROS2 Humble
- Ignition Gazebo 6
- OpenCV
- Python (`rclpy`)
- URDF-based modular drone modeling

The framework focuses on:
- Narrow gap detection
- Navigability score estimation
- Triggered morphological reconfiguration
- Simulation-based drone testing
- Preliminary hardware-level actuation testing

The project was exploratory in nature and developed incrementally from scratch over a period of five months.

---

# 🖥️ Recommended Environment

| Component | Version |
|---|---|
| Operating System | Ubuntu 22.04 LTS |
| ROS Distribution | ROS2 Humble |
| Simulator | Ignition Gazebo 6 |
| Language | Python 3 |
| CV Library | OpenCV |

---

# 📂 Repository Structure

```text
├── narrow_gap/          # Main workspace (gap world, no gravity/dynamics)
├── ng_gravity/         # Workspace with gravity and drone dynamics
├── real_gap/         # Real-world webcam feed integration
├── tunnel_gap/        # Tunnel world testing workspace
├── hardware/         # Hardware testing files (ESP8266 + Servo)
└── README.md
```

---

# 🚀 Workspace Details

---

# 1️⃣ `narrow_gap`
## Main Simulation Workspace

This is the primary workspace used during development.

### Features
- Narrow-gap world environment
- Vision-based narrow gap detection
- Navigability score calculation
- Triggered drone reconfiguration
- Modular drone URDF model
- RViz joint and hinge visualization

### Notes
- Gravity and realistic drone dynamics are disabled
- Focused primarily on validating computer vision and reconfiguration logic

---

## 🔧 Build Workspace

```bash
cd ~/Yash/narrow_gap
rm -rf build install log
colcon build
source install/setup.bash
```

---

## ▶️ Run Simulation

### Terminal 1

```bash
cd ~/Yash/narrow_gap
colcon build
source install/setup.bash
ros2 launch drone_simulation gazebo.launch.py
```

### Terminal 2

```bash
source install/setup.bash
python3 cv_move_drone.py
```

---

## 🧭 Run RViz Visualization

```bash
cd ~/Yash/narrow_gap
ros2 launch drone_description display.launch.py
```

---

# 2️⃣ `ng_gravity`
## Workspace with Gravity and Drone Dynamics

This workspace was created to evaluate the drone under more realistic physical conditions.

### Features
- Gravity enabled
- Drone dynamics enabled
- Narrow gap detection
- Reconfiguration logic retained

### Current Status
Although gap detection and morphological reconfiguration operate correctly, stable drone flight was not achieved in this setup. The drone currently exhibits teleportation-like behavior instead of physically stable flight.

This workspace represents an important experimental stage toward realistic aerial dynamics integration.

---

## ▶️ Run Workspace

### Terminal 1

```bash
cd ~/Yash/ng_gravity
colcon build
source install/setup.bash
ros2 launch drone_simulation gazebo.launch.py
```

### Terminal 2

```bash
source install/setup.bash
python3 cv_move_drone.py
```

---

# 3️⃣ `real_gap`
## Real-World Camera Feed Integration

This workspace was developed to verify whether the gap detection algorithm functions correctly using a real-world camera feed.

A webcam connected to a Windows machine streams video frames to Ubuntu over the local network.

### Features
- Real-world webcam feed integration
- Narrow gap detection using live video
- ROS2 + OpenCV integration
- Network-based frame transmission

### Notes
- Gravity and drone dynamics disabled
- Successfully demonstrated real-world gap detection capability

---

## ▶️ Run Workspace

### Terminal 1

```bash
cd ~/Yash/real_gap
colcon build
source install/setup.bash
ros2 launch drone_simulation gazebo.launch.py
```

### Terminal 2

```bash
source install/setup.bash
python3 cv_move_drone.py
```

---

## 💻 Windows Camera Streaming

First, find the Ubuntu machine IP address:

```bash
ip a
```

Then run the following command on Windows:

```bash
python windows_cam_stream.py --ip <UBUNTU_IP_ADDRESS>
```

---

# 4️⃣ `tunnel_gap`
## Tunnel Environment Workspace

This workspace replaces the narrow walls with a tunnel environment to evaluate reconfiguration behavior in constrained tunnel-like structures.

### Features
- Tunnel-based simulation world
- Navigability score estimation
- Triggered drone reconfiguration
- Successful tunnel traversal experiments

### Notes
- Gravity and realistic dynamics disabled
- Focused on validating adaptability in tunnel environments

---

## ▶️ Run Workspace

### Terminal 1

```bash
cd ~/Yash/tunnel_gap
colcon build
source install/setup.bash
ros2 launch drone_simulation gazebo.launch.py
```

### Terminal 2

```bash
source install/setup.bash
python3 cv_move_drone.py
```

---

# 5️⃣ `hardware`
## Hardware-Level Servo Trigger Testing

This folder contains preliminary hardware implementation code for triggering a servo motor based on narrow-gap detection events.

### Files

| File | Description |
|---|---|
| `test.py` | Python trigger script |
| `servo1.ino` | ESP8266 Arduino code |

---

## 🔌 Hardware Used

- ESP8266 NodeMCU 1.0
- Servo motor
- External power supply

### Serial Port
```text
COM7
```

---

## 🔗 Circuit Connections

| Component | Connection |
|---|---|
| Servo Signal (Yellow) | D1 |
| Servo VCC (Red) | Power Supply + |
| Servo GND (Brown) | Power Supply - |
| NodeMCU GND | Power Supply - |

---

## ✅ Results

The servo motor was successfully triggered based on narrow gap detection events, demonstrating the feasibility of extending the simulation framework toward physical hardware implementation.

---

# 🧠 Key Concepts Implemented

- Vision-based environmental perception
- Narrow gap detection
- HSV/OpenCV-based image processing
- Navigability score estimation
- Morphological drone reconfiguration
- Modular drone URDF modeling
- ROS2 topic communication
- Ignition Gazebo simulation
- Hardware-triggered actuation

---

# ⚠️ Limitations

- Stable aerial dynamics were not fully achieved
- Drone physics behavior requires further refinement
- Reconfiguration currently operates in a simulation-centric framework
- Hardware implementation remains preliminary

---

# 🔮 Future Scope

Potential future extensions include:

- Realistic flight controller integration
- PX4/ArduPilot compatibility
- Reinforcement learning for adaptive navigation
- SLAM-based autonomous exploration
- Real-world modular drone prototype
- Advanced obstacle avoidance
- Dynamic environment adaptation

---

# 📚 Research Context

This work serves as a foundational exploration into:
- Vision-triggered aerial robot adaptation
- Adaptive morphology in UAV systems
- Simulation-driven robotics prototyping
- Intelligent modular drone architectures

The project was developed entirely from scratch without prior robotics background, making it an extensive self-learning and research-oriented effort.

---

# 👨‍💻 Author

**Yash Srivastava**  
B.Tech CSE (AI & ML)  
Manipal Institute of Technology  

Research Internship at  
**Indian Institute of Technology Jodhpur (IIT Jodhpur)**  

---

# 📄 License

This project is intended for academic and research purposes.
