---
title: SEAT, library seat detection
org: Johns Hopkins University
date: Sep – Dec 2018
order: 2
tags: [Computer Vision, Machine Learning]
summary: Uses the library's existing cameras to tell whether a seat is empty, occupied, or held by someone's belongings.
links:
  - { label: Video demo, url: https://www.youtube.com/watch?v=CuB9HgXosaA }
  - { label: Report, url: https://drive.google.com/file/d/13f1mzwg-YVbSFcGfMVgpKGlfl4TwENoi/view?usp=sharing }
  - { label: rexxarchl/library-seat-detection, url: https://github.com/RexxarCHL/library-seat-detection }
---

During exams, students leave their belongings on library seats to hold them and then disappear, so finding a free seat is hard. Occupancy sensors at every seat would be too expensive, but most study areas already have CCTV.

I led a team of three to build a proof-of-concept in Python. We recorded and labeled simulated surveillance footage of a study area from three angles, with four actors. To classify each seat from current and past frames, we combined COCO-pretrained person and chair detectors in TensorFlow with classical OpenCV techniques.

The system reached more than 90% soft accuracy at 10 frames per second in real time.
