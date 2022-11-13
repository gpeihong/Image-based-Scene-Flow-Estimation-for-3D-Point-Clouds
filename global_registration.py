import os
import numpy as np
import open3d as o3d
import time


def draw_registration_result(source, target, transformation):
    source.paint_uniform_color([1, 0.706, 0])
    target.paint_uniform_color([0, 0.651, 0.929])
    source.transform(transformation)
    o3d.visualization.draw_geometries([source, target])


def preprocess_point_cloud(pcd, voxel_size):
    print(":: 使用大小为为{}的体素下采样点云.".format(voxel_size))
    pcd_down = o3d.voxel_down_sample(pcd, voxel_size)

    radius_normal = voxel_size * 2
    print(":: 使用搜索半径为{}估计法线".format(radius_normal))
    o3d.estimate_normals(pcd_down, o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    radius_feature = voxel_size * 5
    print(":: 使用搜索半径为{}计算FPFH特征".format(radius_feature))
    pcd_fpfh = o3d.registration.compute_fpfh_feature(pcd_down, o3d.geometry.KDTreeSearchParamHybrid(
        radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh


def prepare_dataset(voxel_size):
    print(":: 加载点云并转换点云的位姿.")
    source = o3d.io.read_point_cloud("./new_0000000000.ply")
    target = o3d.io.read_point_cloud("./new_0000000001.ply")
    trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
    source.transform(trans_init)
    # draw_registration_result(source, target, np.identity(4))

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh


# def execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size):
#     distance_threshold = voxel_size * 1.5
#     print(":: 对下采样的点云进行RANSAC配准.")
#     print("   下采样体素的大小为： %.3f," % voxel_size)
#     print("   使用宽松的距离阈值： %.3f." % distance_threshold)
#     result = o3d.registration.registration_ransac_based_on_feature_matching(
#         source_down, target_down, source_fpfh, target_fpfh, True, distance_threshold,
#         o3d.registration.TransformationEstimationPointToPoint(False), 3,
#         [o3d.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
#          o3d.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)
#          ], o3d.registration.RANSACConvergenceCriteria(100000, 0.999))
#     return result
def execute_fast_global_registration(source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size):
    distance_threshold = voxel_size * 80
    print(":: 基于距离阈值为 %.3f的快速全局配准" % distance_threshold)
    result = o3d.registration.registration_fast_based_on_feature_matching(source_down, target_down,
                                                                          source_fpfh, target_fpfh,
                                                                          o3d.registration.FastGlobalRegistrationOption(
                                                                              maximum_correspondence_distance=distance_threshold))
    return result


def refine_registration(source, target, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 80
    print(":: 对原始点云进行点对面ICP配准精细对齐， 这次使用严格的距离阈值： %.3f." % distance_threshold)
    result = o3d.registration.registration_icp(source, target, distance_threshold, result_fast.transformation,
                                               o3d.registration.TransformationEstimationPointToPlane())
    return result


# 相当于使用5cm的体素对点云进行均值操作
voxel_size = 10  # means 5cm for this dataset
source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(voxel_size)
start = time.time()
result_fast = execute_fast_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size)
print(result_fast.correspondence_set)
print("快速全局配准花费了： %.3f 秒.\n" % (time.time() - start))
print(result_fast.correspondence_set)
draw_registration_result(source_down, target_down, result_fast.transformation)
result_icp = refine_registration(source, target, source_fpfh, target_fpfh, voxel_size)
# print("局部配准花费了： %.3f 秒.\n" % (time.time() - start))
# print(result_icp)
draw_registration_result(source, target, result_icp.transformation)