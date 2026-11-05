# 🤖 OpenCV Gesture-Controlled Robot in Gazebo | ROS 2

A vision-based robot control project that integrates **OpenCV, Python, ROS 2 and Gazebo** to enable robot movement through hand gestures.

The project explores Human-Robot Interaction (HRI) by using computer vision to recognize hand gestures and translate them into robot movement commands in a simulated environment.

##  Project Overview

This project demonstrates how hand gestures can be used as an alternative input method for controlling a mobile robot.

A camera captures real-time hand movements, OpenCV processes the camera frames, and the recognized gestures are converted into velocity commands. These commands are communicated through ROS 2 to control the robot inside the Gazebo simulation environment.

##  Features

- Real-time camera input using OpenCV.
- Hand gesture detection and recognition.
- Gesture-based robot movement control.
- ROS 2 communication for sending velocity commands.
- Mobile robot simulation using Gazebo.
- Human-Robot Interaction through computer vision.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| OpenCV | Image processing and gesture detection |
| ROS 2 Humble | Robot communication and control |
| Gazebo | Robot simulation |
| Linux Ubuntu 22.04 | Development environment |

## ⚙️ System Architecture

```text
        Webcam
           |
           v
    Camera Frame Capture
           |
           v
      OpenCV Processing
           |
           v
   Hand Gesture Recognition
           |
           v
   Gesture-to-Motion Mapping
           |
           v
       ROS 2 Node
           |
           v
    Velocity Commands
      (cmd_vel)
           |
           v
    Gazebo Simulation
           |
           v
      Robot Movement
```

## 📂 Project Structure

```text
opencv-gesture-control-gazebo-robot/
│
├── src/
│   └── robot_pkg/
│       ├── robot_pkg/
│       ├── launch/
│       ├── package.xml
│       └── setup.py
│
├── .gitignore
└── README.md
```

*Note: The structure above is a general overview. Adjust it to match the actual files in your repository.*

## 📋 Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- OpenCV
- Gazebo
- Webcam

## 🔧 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/akhilranand/opencv-gesture-control-gazebo-robot.git
```

### 2. Navigate to the Workspace

```bash
cd opencv-gesture-control-gazebo-robot
```

### 3. Install Dependencies

```bash
sudo apt update
sudo apt install python3-opencv
```

Ensure that ROS 2 Humble and the required Gazebo packages are installed.

### 4. Build the ROS 2 Workspace

```bash
source /opt/ros/humble/setup.bash

colcon build
```

### 5. Source the Workspace

```bash
source install/setup.bash
```

### 6. Run the Project

Launch the Gazebo simulation and start the gesture recognition and robot control nodes using the appropriate launch files or ROS 2 run commands in the package.

## 🎯 Project Objective

The main objective is to develop a vision-based control interface that allows humans to interact with a simulated mobile robot using natural hand gestures.

This project provides practical experience in:

- Computer Vision
- Image Processing
- ROS 2 Nodes and Topics
- Robot Motion Control
- Gazebo Simulation
- Human-Robot Interaction

## 👨‍💻 Author

**Akhil R Anand**

Robotics and Automation Engineer

- GitHub: [@akhilranand](https://github.com/akhilranand)
- Project Repository: [OpenCV Gesture-Controlled Gazebo Robot](https://github.com/akhilranand/opencv-gesture-control-gazebo-robot)

---

⭐ If you find this project interesting, consider giving the repository a star!