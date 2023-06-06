AI-project
===

[**通過系計中運算資源貢獻此專案**](https://hackmd.io/@oceanic/BywRXeyNn)

[**Github Page 使用教學**](https://www.youtube.com/watch?v=NovKS8kWYAg)

To do
---
- [x] Design the project
- [x] Organize codebase and design architecture
- [x] Prepare dataset
- [x] Design the program
- [x] Define evaluation matrices
- [ ] Qualitative and quantitative testing
- [ ] Write report

Due
---
- [x] Provide a 1-2 page slides to summarize your progress: 5/9
- [x] Construct a GitHub repo for your project: 5/9
- [ ] Presentation deadline: 6/9

Video synthesis with near-duplicate images
---
- An app selecting and merging near-duplicate images.
### Strategies
We can make a program that provides several functionalities:
- Generating mid frames among near-duplicate images
- Apply motion sculpture algorithm
- Output gif

#### Codebase
1. Generating videos
    - https://github.com/google-research/frame-interpolation
2. Deformable sprites
    - https://github.com/vye16/deformable-sprites

Demo
---
[![Demo-v2motion_sculpture.ipynb](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Crowded-dorm/AI-Final-Project/blob/main/Demo_near-duplicate-synthesis.ipynb) Colab demo for generating motion-sculpture effect video from near-duplicate images!  
[![Demo-v2motion_sculpture.ipynb](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Crowded-dorm/AI-Final-Project/blob/main/Demo_v2motion_sculpture.ipynb) Colab demo for generating motion-sculpture effect from an input video.

Evaluation metrices
---
- Intersection over union (IoU)
    - UnitBox: An Advanced Object Detection Network
- Boundary IoU: Improving Object-Centric Image Segmentation Evaluation

Results
---


分工
---
