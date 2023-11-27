The authors present a **KITTI Object Detection** dataset (is a part of a larger **KITTI** dataset) obtained from a VW station wagon for application in mobile robotics and autonomous driving research. They meticulously recorded 6 hours of traffic scenarios at 10–100 Hz, utilizing a range of sensor modalities, including high-resolution color and grayscale stereo cameras, a Velodyne 3D laser scanner, and a high-precision GPS/IMU inertial navigation system. The dataset encompasses diverse scenarios, capturing real-world traffic situations across freeways, rural areas, and inner-city scenes with numerous static and dynamic objects. The data is calibrated, synchronized, timestamped, and provided in rectified and raw image sequences. Additionally, the dataset contains object labels in the form of 3D tracklets, and the authors offer online benchmarks for stereo, optical flow, object detection, and other tasks. The paper details the recording platform, data format, and utilities provided by the authors.


<img src="https://github.com/dataset-ninja/kitti-object-detection/assets/78355358/37cf0281-3e3e-4b9f-9b8e-ff2e57dfc20f" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Recording platform. The VW Passat station wagon is equipped with four video cameras (two color and two grayscale cameras), a rotating 3D laser scanner and a combined GPS/IMU inertial navigation system.</span>

The KITTI dataset, recorded from a moving platform around Karlsruhe, Germany, includes camera images, laser scans, high-precision GPS measurements, and IMU accelerations. Its primary objective is to advance the development of computer vision and robotic algorithms for autonomous driving.

The dataset includes specifications for cameras, lenses, laser scanner, and inertial and GPS navigation system. Notably, the color cameras exhibit limitations in resolution due to the Bayer pattern interpolation process and reduced sensitivity to light. Two stereo camera rigs are employed, one for grayscale and one for color, each with a baseline of approximately 54 cm. 


<img src="https://github.com/dataset-ninja/kitti-object-detection/assets/78355358/7e8a1ff3-a67f-40fb-87e6-a20fccbefdc0" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Sensor setup. This figure illustrates the dimensions and mounting positions of the sensors (red) with respect to the vehicle body. Heights above ground are marked in green and measured with respect to the road surface. Transformations between sensors are shown in blue.</span>

The raw data constitutes approximately 25% of the overall recordings. The dataset includes sequences categorized as 'Road,' 'City,' 'Residential,' 'Campus,' and 'Person.' Each sequence is accompanied by raw data, object annotations in the form of 3D bounding box tracklets, and a calibration file. Example frames are illustrated, and recordings occurred on specific dates in September and October 2011 during daytime, resulting in a dataset size of 180 GB.

<img src="https://github.com/dataset-ninja/kitti-object-detection/assets/78355358/a6bb973b-204f-4307-a6f8-d5bffd8b0e30" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Object coordinates. This figure illustrates the coordinate system of the annotated 3D bounding boxes with respect to the coordinate system of the 3D Velodyne laser scanner. In z-direction, the object coordinate system is located at the bottom of the object (contact point with the supporting surface).</span>

Annotations for dynamic objects within the reference camera’s field of view are provided in the form of 3D bounding box tracklets, represented in Velodyne coordinates. Object classes include *car*, *van*, *truck*, *pedestrian*, and others. Each object is assigned a class and its 3D ***dimensions*** (height, width, length), along with translation and ***rotation y*** information in 3D for each frame. The development kit contains C++/MATLAB code for reading and writing tracklets.

To offer further insights into the dataset's properties, statistics for sequences with annotated objects are provided. Figures show the total number of objects, object orientations, object labels per image, sequence length, and egomotion of the platform recorded by the GPS/IMU system. Statistics are presented for the whole dataset and per street category.

<img src="https://github.com/dataset-ninja/kitti-object-detection/assets/78355358/d7e89e0f-1214-4b05-8be2-a6ed4ef87670" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Number of object labels per class and image. This figure shows how often an object occurs in an image.</span>
