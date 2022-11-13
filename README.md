# Image-based-Scene-Flow-Estimation-for-3D-Point-Clouds
Project in DUT Media Lab

## Abstract
In recent years, with the development and popularity of 3D scanning devices, 3D data such as point clouds have appeared in people's lives and are growing explosively, and the scene flow estimation for point clouds has become a hot research topic today. The 3D motion field formed by the scene motion in space is called scene flow. Scene flow estimation has important research significance in the fields of target detection, virtual reality, scene understanding, and scene dynamic reconstruction. 

Most of the current research work on point cloud scene flow is based on deep learning, where point clouds are learned by end-to-end neural networks. Although these deep learning methods have achieved better results than traditional methods, they still face some bottlenecks. Due to the lack of practical data (marking cost is too high) and objective evaluation metrics, there is still a long way to go before engineering applications. In addition, scene flow estimation has been affected by the speed of computing due to the large spatial scale of calculation. And the huge amount of computation brought by point clouds is also an important factor limiting the scene flow research. 

To address the above problems, this paper proposes a method to combine optical flow estimation to achieve 3D point cloud scene flow estimation. First, the FlowNet [2] network is trained on the KITTI dataset and the trained model is used to perform the optical flow estimation task to generate the desired optical flow images. Based on the correspondence that the projection of the scene flow in the 2D image plane is the optical flow, the camera intrinsic matrix, the rotation matrix from the reference camera to the target camera image plane, and the extrinsic matrix from the LiDAR to the reference camera are applied to calculate the projection matrix, and the point cloud is projected onto the corresponding image to achieve the sensor fusion. Finally, combined with the ICP registration of the point clouds, the lines between all corresponding point pairs between adjacent two frames of point clouds are drawn, and combined with the optical flow information of the image, the point cloud scene flow
estimation and visualization with low amount of computation are realized.
