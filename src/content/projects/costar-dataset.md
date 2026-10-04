---
title: CoSTAR Block Stacking Dataset
org: Johns Hopkins University
date: Sep 2018 – Mar 2019
order: 1
tags: [Robotics, Machine Learning]
summary: A robotic grasping and stacking dataset with more than 10k attempts and 2M frames, published at IROS 2019.
links:
  - { label: Paper (arXiv:1810.11714), url: https://arxiv.org/abs/1810.11714 }
  - { label: Dataset website, url: https://sites.google.com/site/costardataset }
  - { label: ahundt/costar_dataset, url: https://github.com/ahundt/costar_dataset }
  - { label: jhu-lcsr/costar_plan, url: https://github.com/jhu-lcsr/costar_plan }
---

Model-based perception and planning let robots grasp objects reliably in structured settings, but learned approaches can fail on a simple block-stacking task once conditions get even slightly more realistic. Existing manipulation datasets also didn't capture end-to-end task planning with obstacle avoidance.

The CoSTAR Block Stacking Dataset lets researchers study how learning systems handle workspace constraints, using a robot that grasps and stacks colored blocks.

**My part:** I wrote the data loader, training scripts and visualization tools, packaged them on PyPI for TensorFlow and PyTorch, and added documentation, examples and training splits. Batch loading got up to 80% faster, which cut a 200-epoch training run from 800+ hours to about 200.

A. Hundt, V. Jain, **C. H. Lin**, C. Paxton, and G. D. Hager, "The CoSTAR Block Stacking Dataset: Learning with Workspace Constraints," IROS 2019.
