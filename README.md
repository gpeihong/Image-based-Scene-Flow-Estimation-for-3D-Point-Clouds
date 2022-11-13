# Image-based-Scene-Flow-Estimation-for-3D-Point-Clouds
Project in DUT Media Lab

## Abstract
In recent years, with the development and popularity of 3D scanning devices, 3D data such as point clouds have appeared in people's lives and are growing explosively, and the scene flow estimation for point clouds has become a hot research topic today. The 3D motion field formed by the scene motion in space is called scene flow. Scene flow estimation has important research significance in the fields of target detection, virtual reality, scene understanding, and scene dynamic reconstruction. 

Most of the current research work on point cloud scene flow is based on deep learning, where point clouds are learned by end-to-end neural networks. Although these deep learning methods have achieved better results than traditional methods, they still face some bottlenecks. Due to the lack of practical data (marking cost is too high) and objective evaluation metrics, there is still a long way to go before engineering applications. In addition, scene flow estimation has been affected by the speed of computing due to the large spatial scale of calculation. And the huge amount of computation brought by point clouds is also an important factor limiting the scene flow research. 

To address the above problems, this paper proposes a method to combine optical flow estimation to achieve 3D point cloud scene flow estimation. First, the FlowNet [2] network is trained on the KITTI dataset and the trained model is used to perform the optical flow estimation task to generate the desired optical flow images. Based on the correspondence that the projection of the scene flow in the 2D image plane is the optical flow, the camera intrinsic matrix, the rotation matrix from the reference camera to the target camera image plane, and the extrinsic matrix from the LiDAR to the reference camera are applied to calculate the projection matrix, and the point cloud is projected onto the corresponding image to achieve the sensor fusion. Finally, combined with the ICP registration of the point clouds, the lines between all corresponding point pairs between adjacent two frames of point clouds are drawn, and combined with the optical flow information of the image, the point cloud scene flow estimation and visualization with low amount of computation are realized.

## Training of the neural network
Two datasets, MPI Sintel and Flying Chairs are used. MPI Sintel data formats include .flo, .png; FlyingChairs include .ppm, .png. Find image pair positions by data source type and save the positions by group within List, then break the dataset into training and validation groups. After the model training, the test is executed on the MPI Sintel dataset using the currently trained model with an EPE of 1.485, similar to the test results in the original paper. Figure 3.8 shows the test visualization results, and Figure 3.9 shows its corresponding ground truth.

Testing results in MPI Sintel：

![image](https://user-images.githubusercontent.com/95701078/201511189-9136eeb0-847c-40b4-bf96-bbb1c5928686.png)

MPI Sintel Ground Truth：

![image](https://user-images.githubusercontent.com/95701078/201511195-c819561f-9500-4923-b41c-97c0dfdc05ce.png)
### Optical flow estimation of Kitti Road：
Input image pair：

![image](https://user-images.githubusercontent.com/95701078/201511073-bf237298-2724-4053-9e93-a031bd5ce33f.png)
![image](https://user-images.githubusercontent.com/95701078/201511075-08b9644c-a463-4dc9-bac9-229d97fb000e.png)

Output color coded flow field：

![image](https://user-images.githubusercontent.com/95701078/201511077-b8f0c197-c372-4a7b-8c03-5464d23b2378.png)

## Fusion of sensors
Sensor setup[39]：

![image](https://user-images.githubusercontent.com/95701078/201511620-491be2b7-c231-4a7f-900c-c8c90297692f.png)

Object coordinates[39]:

![image](https://user-images.githubusercontent.com/95701078/201511646-0fa7e2cc-f87a-4626-bc94-7a82fc0150e2.png)

The transformation relation is shown as follows:

![image](https://user-images.githubusercontent.com/95701078/201511714-f0e515fd-5a2b-4355-9396-7526fa02b678.png)

Where Tr_velo_to_cam * X is the projection of point X in Velodyne point cloud coordinates into the camera 00 (reference camera) coordinate system. R_rect00 *Tr_velo_to_cam * X is the projection of the point X in Velodyne coordinates into the camera 00 (reference camera) coordinate system, and the image coplanar alignment correction based on the reference camera 00, which is necessary for 3D projection using the KITTI dataset. P_rect_00 * R_rect00 * Tr_velo_to_cam * X is to project the point X in Velodyne coordinates into the camera 00 (reference camera) coordinate system, then perform the image co-alignment correction, and then project it into the pixel coordinate system of camera xx.

Point cloud P1 after removing points outside the image plane:

![image](https://user-images.githubusercontent.com/95701078/201511753-40d7d508-6958-4d38-9260-4ad5d683aa3d.png)

Projection of P1 to image P after removal of some points:

![image](https://user-images.githubusercontent.com/95701078/201511769-8a237994-c1dc-4f52-baa4-b25482dbef42.png)


