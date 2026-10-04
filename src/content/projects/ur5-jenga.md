---
title: UR5 Plays Jenga
org: Johns Hopkins University
date: Feb – May 2018
order: 3
tags: [Robotics, Hardware, ROS]
summary: A UR5 arm with a custom sensing end-effector that plays Jenga on its own, up to 20 levels.
links:
  - { label: Video demo, url: https://www.youtube.com/watch?v=KtRhFWFU7mw }
  - { label: Report, url: https://drive.google.com/file/d/16NKua-MJHY3XStXdP2z2SLvy-ZEi5fuj/view?usp=sharing }
  - { label: rexxarchl/UR5_Plays_Jenga, url: https://github.com/RexxarCHL/UR5_Plays_Jenga }
---

Robots have played Jenga since at least 2008 ([Kröger et al., "A manipulator plays Jenga"](https://ieeexplore.ieee.org/document/4624586)), but those systems relied on proprietary software, custom communication links and up to four control computers. I wanted to see how much easier it would be with modern compute and ROS. Also, playing Jenga alone is boring.

I designed and built a custom end-effector in PTC Creo and Autodesk EAGLE. It has a micro load cell that senses loose blocks and pushes one out, a micro LiDAR that locates the block, and a rack-and-pinion gripper that extracts the block and places it on top.

The software is about 3,000 lines of C++ on ROS, plus Python, MATLAB and Arduino. It covers camera calibration, end-effector control on an Arduino UNO, a Jenga-playing AI, and arm trajectory control.

The robot plays a block in about a minute and has reached 20 levels before the tower fell.
