import os
import open3d as o3d
import numpy as np

print("Load a ply point cloud, print it, and render it")
pcd1 = o3d.io.read_point_cloud("./0000000008.ply")
point_array = np.asarray(pcd1.points)
print(point_array)
length = len(point_array)
index = []

for i in range(length):
    if point_array[i][2] < -161 or point_array[i][0] < 1200 or point_array[i][1] < -1100 or point_array[i][2] > 950:
        index.append(i)
new_array = np.delete(point_array, index, axis=0)
print(new_array)
new_pcd1 = o3d.geometry.PointCloud()
new_pcd1.points = o3d.utility.Vector3dVector(new_array)
new_pcd1.paint_uniform_color([1, 0.706, 0])
o3d.visualization.draw_geometries([new_pcd1])
o3d.io.write_point_cloud("./cut_0000000008.ply", new_pcd1)
