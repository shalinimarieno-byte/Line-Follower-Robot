# Line Follower Robot

A ROS 2-based autonomous mobile robot designed to follow a predefined path using sensor-based line detection.

The project demonstrates the implementation of sensor-based control logic for autonomous robot movement.

## Features

- Autonomous line following
- Real-time path detection
- Sensor-based control
- Differential-drive movement
- ROS 2 integration
- Gazebo simulation
- Custom robot model
- Custom line-track environment

## Technologies Used

- ROS 2
- Python
- Gazebo
- RViz2
- URDF / Xacro
- Sensor-based line detection
- Differential Drive

## System Requirements

| Component | Requirement |
|---|---|
| Operating System | Ubuntu 24.04 |
| ROS 2 | Jazzy |
| Python | Python 3 |
| Gazebo | Gazebo Sim |

## Project Structure

```text
Line-Follower-Robot/
│
└── src/
    └── line_follower_bot/
        ├── launch/
        │   └── line_bot.launch.py
        │
        ├── scripts/
        │   └── line_follower.py
        │
        ├── urdf/
        │   └── line_bot.urdf.xacro
        │
        ├── worlds/
        │   └── line_track.sdf
        │
        ├── test/
        ├── resource/
        ├── package.xml
        ├── setup.py
        └── setup.cfg
