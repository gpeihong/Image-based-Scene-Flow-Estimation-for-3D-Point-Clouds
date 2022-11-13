import open3d as o3d
import numpy as np
import scipy.io as sio
from PIL import Image

# 读取电脑中的 ply 点云文件
source = o3d.read_point_cloud("./new_0000000007.ply")  # source 为需要配准的点云
source_cut = o3d.read_point_cloud("./cut_0000000007.ply")
target = o3d.read_point_cloud("./new_0000000008.ply")  # target 为目标点云
target_cut = o3d.read_point_cloud("./cut_0000000008.ply")
# 为两个点云上上不同的颜色
source.paint_uniform_color([1, 0.706, 0])  # source 为黄色
target.paint_uniform_color([0, 0.651, 0.929])  # target 为蓝色
# 为两个点云分别进行outlier removal
processed_source, outlier_index = o3d.geometry.radius_outlier_removal(source,
                                                                      nb_points=3,
                                                                      radius=55)

processed_target, outlier_index = o3d.geometry.radius_outlier_removal(target,
                                                                      nb_points=3,
                                                                      radius=55)
processed_source_cut, outlier_index = o3d.geometry.radius_outlier_removal(source_cut,
                                                                      nb_points=3,
                                                                      radius=55)
processed_target_cut, outlier_index = o3d.geometry.radius_outlier_removal(target_cut,
                                                                      nb_points=3,
                                                                      radius=55)
processed_target_cut.paint_uniform_color([0, 0.651, 0.929])
threshold = 120  # 移动范围的阀值
trans_init = np.asarray([[1, 0, 0, 0],  # 4x4 identity matrix，这是一个转换矩阵，
                         [0, 1, 0, 0],  # 象征着没有任何位移，没有任何旋转，我们输入
                         [0, 0, 1, 0],  # 这个矩阵为初始变换
                         [0, 0, 0, 1]])

# 运行icp
reg_p2p = o3d.registration.registration_icp(
    processed_source, processed_target, threshold, trans_init,
    o3d.registration.TransformationEstimationPointToPoint(),
    o3d.registration.ICPConvergenceCriteria(max_iteration=100))

# 输出对应点索引组成的列表
a = np.asarray(reg_p2p.correspondence_set)
print(f"总配准点对数：{len(a)}")
correspondence_list = []
for i in range(len(a)):
    correspondence_list.append(tuple(a[i]))
print(f"两针点云对应点索引组成的列表为:\n{correspondence_list}")

# 输出连线点对应的的实际坐标
b = np.asarray(processed_source.points)
real_points = []
for i in range(len(a)):
    c = b[a[i][0]] / 100
    real_points.append(c)
print(f"源点源参与配准连线的实际坐标是：\n{np.asarray(real_points)}")

# 寻找第一帧x>=12.00的实际坐标和对应点索引列表(使点云在之后的投影中完全投影至图像内部)
new_real_points = []
new_correspondence_list = []
for i in range(len(real_points)):
    if real_points[i][0] >= 12 and real_points[i][1] <= 9.5 and real_points[i][1] >= -11:
        new_real_points.append(real_points[i])
        new_correspondence_list.append(a[i])
print(f"缩小范围后的实际坐标是：\n{np.asarray(new_real_points)}")
# print(np.asarray(new_correspondence_list))
len_new_correspondence_list = len(new_correspondence_list)
print(f"对应点连线总数：{len_new_correspondence_list}")
# 转换matlab矩阵为numpy矩阵
load_data = sio.loadmat('velo.mat')
matrix_velo = load_data['velo']
load_data2 = sio.loadmat('velo_img.mat')
# print(load_data2.keys())
matrix_velo_img = load_data2['velo_img']

# 寻找连线点对应的投影点
correspondence_mat = []
for i in range(len(new_real_points)):
    for j in range(len(matrix_velo)):
        if abs(new_real_points[i][0] - matrix_velo[j][0]) <= 0.01 and abs(
                new_real_points[i][1] - matrix_velo[j][1]) <= 0.01 and abs(
                new_real_points[i][2] - matrix_velo[j][2]) <= 0.01:
            correspondence_mat.append(j)
print(f"matlab中对应的点的索引序号是：\n{correspondence_mat}")
len_correspondence_mat = len(correspondence_mat)
print(f"因为数据读取的偏差，matlab中源点源实际的数目为：{len_correspondence_mat}")

# processed_source.transform(reg_p2p.transformation)
lineset = o3d.create_line_set_from_point_cloud_correspondences(processed_source, processed_target,
                                                               new_correspondence_list)
axis = o3d.geometry.create_mesh_coordinate_frame(size=50, origin=[0, 0, -169])
# lineset上色
# 打开要处理的图像
img_src = Image.open('./0000000007img_flow.png')
# 转换图片的模式为RGB
img_src = img_src.convert('RGB')
# 获得文字图片的每个像素点
src_strlist = img_src.load()
# 结果是一个元组包含这个像素点的颜色信息 eg:(0, 0, 0)
lineset_color_list = []
for i in range(len(correspondence_mat)):
    single_color_list = list(
        src_strlist[matrix_velo_img[correspondence_mat[i]][0], matrix_velo_img[correspondence_mat[i]][1]])
    new_single_color_list = [j / 255 for j in single_color_list]
    lineset_color_list.append(new_single_color_list)
for i in range(len_new_correspondence_list - len_correspondence_mat):
    lineset_color_list.append([1, 0.99, 0.9])
# lineset_color_array=np.asarray(lineset.colors)

# print(lineset_color_list)
lineset_color_array = np.array(lineset_color_list)
print(f"全部线条的颜色值为:\n{lineset_color_array}")
# print(lineset_color_array)
lineset.colors = o3d.utility.Vector3dVector(lineset_color_array)
# 创建一个 o3d.visualizer class
vis = o3d.visualization.Visualizer()
vis.create_window()

# 将两个点云放入visualizer
vis.add_geometry(processed_source_cut)
# vis.add_geometry(processed_target_cut)
vis.add_geometry(lineset)
vis.add_geometry(axis)
# 让visualizer渲染点云
vis.update_geometry()
vis.poll_events()
vis.update_renderer()

vis.run()
