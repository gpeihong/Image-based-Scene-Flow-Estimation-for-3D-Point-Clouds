import open3d as o3d
import numpy as np
#读取电脑中的 ply 点云文件
source = o3d.read_point_cloud("./0000000007.ply")  #source 为需要配准的点云
target = o3d.read_point_cloud("./cut_0000000008.ply")  #target 为目标点云

#为两个点云上上不同的颜色
source.paint_uniform_color([1, 0.706, 0])    #source 为黄色
target.paint_uniform_color([0, 0.651, 0.929])#target 为蓝色
# lineset = o3d.create_line_set_from_point_cloud_correspondences(source, target, [(1,2),(3,4),(6,7)])

#创建一个 o3d.visualizer class
vis = o3d.visualization.Visualizer()
vis.create_window()

#将两个点云放入visualizer
# vis.add_geometry(source)
vis.add_geometry(target)
# vis.add_geometry(lineset)
#让visualizer渲染点云
vis.update_geometry()
vis.poll_events()
vis.update_renderer()

vis.run()
