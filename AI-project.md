AI-project
===

To do
---
- [x] Design the project
- [ ] Organize codebase and design architecture
- [ ] Prepare dataset
- [ ] Design the program
- [ ] Testing and debug
- [ ] Write report

Due
---
- [ ] Provide a 1-2 page slides to summarize your progress: 5/9
- [ ] Construct a GitHub repo for your project: 5/9
- [ ] Showcase your final project: 6/6, tentatively

Video synthesis with near-duplicate images
---
- [x] An app selecting and merging near-duplicate images.
### Strategies
We can build an app that provides several functionalities:
- Find near-duplicate images
- Ask Users to select the images to merge to a video or delete.
- Output a merged video
- (Bonus) Control the camera to make video viewpoint move! (3d-moments)

#### Codebase
1. Detecting near-duplicate images

- https://github.com/idealo/imagededup
```python=
from imagededup.methods import PHash
phasher = PHash()
encodings = phasher.encode_images(image_dir='path/to/image/directory')
duplicates = phasher.find_duplicates(encoding_map=encodings)
```

2. Generating videos (The second one can control the camera.)
- https://github.com/google-research/frame-interpolation
- https://3d-moments.github.io/

### Resource
[Image duplicate detection](https://github.com/topics/image-duplicate-detection)
[Video editor](https://github.com/topics/video-editor)