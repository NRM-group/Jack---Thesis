#!/usr/bin/python3

from debugpy import listen
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.decomposition import PCA
from mpl_toolkits import mplot3d
from scipy.spatial import ConvexHull
from pyvista import PolyData
import open3d as o3d

def check_bounds(X_raw, n):
    return (X_raw[n, 0] >= 1 or X_raw[n, 0] <= -0.1 or X_raw[n, 1] >= 0.48 or X_raw[n, 1] <= -0.1 or X_raw[n, 2] >= 2 or X_raw[n, 2] <= 0.9) or (X_raw[n, 0] < 0.2 and X_raw[n, 1] > 0.4)

def hullToSurface(hull):
    faces = np.column_stack((3*np.ones((len(hull.simplices), 1), dtype=int), hull.simplices)).flatten()
    surface = PolyData(hull.points, faces)
    return surface

def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud],
                                      zoom=0.3412,
                                      front=[0.4257, -0.2125, -0.8795],
                                      lookat=[2.6172, 2.0475, 1.532],
                                      up=[-0.0694, -0.9768, 0.2024])

def visualise_pcl(pcl):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pcl)
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[0, 0, 0])
    o3d.visualization.draw_geometries([pcd, mesh_frame])
    

def filter_outliers(pcl):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pcl)
    # voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.02)
    # cl, ind = voxel_down_pcd.remove_statistical_outlier(nb_neighbors=np.size(pcl[0]),
                                                        # std_ratio=2.0)
    cl, ind = pcd.remove_radius_outlier(nb_points=8, radius=0.15)
    pcl_filt = np.asarray(cl.points)    
    return pcl_filt

def pcl_to_3d(pcl):
    ax_3d = plt.axes(projection='3d')
    ax_3d.scatter3D(pcl[:, 0], pcl[:, 1], pcl[:, 2]);
    hull = ConvexHull(pcl)
    for s in hull.simplices:
        s = np.append(s, s[0])
        ax_3d.plot(pcl[s, 0], pcl[s, 1], pcl[s, 2], "r-")
    ax_3d.set_xlabel('X (m)')
    ax_3d.set_ylabel('Y (m)')
    ax_3d.set_zlabel('Z (m)')
    plt.show()

def pcl_to_pca(pcl):
    pca = PCA(n_components=2)
    pca.fit(pcl)
    Y = pca.transform(pcl)
    ax_2d = plt.axes()
    plt.scatter(Y[:, 0], Y[:, 1]);
    ax_2d.set_xlabel('Component 1')
    ax_2d.set_ylabel('Component 2')    
    plt.show()
    
if __name__ == "__main__":
    X_raw = np.genfromtxt(r'/home/medrobotics/jack_ws/src/mrn_movo/data/test_miguel_3_saved.csv', delimiter=',')
    X_raw_chest = X_raw[1:, :3]
    X_raw_wrist_left = X_raw[1:, 3:6]
    X_raw_wrist_right = X_raw[1:, 6:9]
    X_raw_chest_wrist_right = X_raw_wrist_right - X_raw_chest
    
    wrist_right_not_zeros = ~np.all(X_raw_wrist_right == 0, axis=1)
    chest_not_zeros = ~np.all(X_raw_chest == 0, axis=1)
    wrist_right_chest_not_zeros = np.logical_and(wrist_right_not_zeros, chest_not_zeros)
    
    # remove rows having all zeroes
    X_raw_chest_wrist_right = X_raw_chest_wrist_right[wrist_right_chest_not_zeros]
    X_raw_chest_wrist_right[:, 0] = -1 * X_raw_chest_wrist_right[:, 0]
    X_raw_chest_wrist_right[:, 1] = -1 * X_raw_chest_wrist_right[:, 1]
    
    # X_raw_chest_wrist_right = np.delete(X_raw, X_raw[:,2] > 2, axis=0)
    
    X_filt = filter_outliers(X_raw_wrist_right)

    x_min = 0.0
    x_max = 0.45
    y_min = -0.6
    y_max = 0
    z_min = 0.0
    z_max = 0.45
    
    X, Y, Z = np.meshgrid(
        np.linspace(x_min, x_max, 15),
        np.linspace(y_min, y_max, 15),
        np.linspace(z_min, z_max, 15)
    )
    xyz = np.vstack((X.flatten(), Y.flatten(), Z.flatten())).T
    
    
    # X_filt[:, 2] = -1 * X_filt[:, 2]
    
    # fig1 = plt.figure(1)
    # pcl_to_3d(X_filt)
    
    # # fig2 = plt.figure(2)
    # # pcl_to_pca(X_filt)
    
    # hullToSurface(ConvexHull(X_filt)).plot()
    
    # visualise_pcl(X_raw_chest_wrist_right)
    # visualise_pcl(X_filt)

    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(X_filt)
    # pcd_cube = o3d.geometry.PointCloud()
    # pcd_cube.points = o3d.utility.Vector3dVector(xyz)
    
    # mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[0, 0, 0])
    # o3d.visualization.draw_geometries([pcd, pcd_cube, mesh_frame])
    
    # pcd.estimate_normals(
    # search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    
    
    alpha = 0.3
    radii = [0.005, 0.01, 0.02, 0.04]
    print(f"alpha={alpha:.3f}")
    
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
    mesh.compute_vertex_normals()
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[0, 0, 0])
    o3d.visualization.draw_geometries([mesh, mesh_frame], mesh_show_back_face=True)
    # volume = o3d.geometry.TriangleMesh.get_volume(mesh)
    # print(volume)
    o3d.io.write_triangle_mesh("miguel_3.ply", mesh)
    surface_area = o3d.geometry.TriangleMesh.get_surface_area(mesh)
    
    fig = plt.figure()
    ax =  fig.add_subplot(111)
    data_jack = np.array([0.03578766801815441, 0.058, 0.0745773768502948, 0.040326225014803655, 0.04257842653133096])
    print(np.mean(data_jack))
    data_jack_diff = [data_jack[0]-data_jack[1],
                      data_jack[0]-data_jack[2],
                      data_jack[0]-data_jack[3],
                      data_jack[0]-data_jack[4],
                      data_jack[1]-data_jack[2],
                      data_jack[1]-data_jack[3],
                      data_jack[1]-data_jack[4],
                      data_jack[2]-data_jack[3],
                      data_jack[2]-data_jack[4],
                      data_jack[3]-data_jack[4]]
    abs_jack =  [abs(ele) for ele in data_jack_diff]
    print(np.mean(abs_jack))
    print(np.median(abs_jack))
    q75, q25 = np.percentile(abs_jack, [75, 25])
    print("q75: %s"%q75)
    print("q25: %s"%q25)
    # matplotlib.pyplot.boxplot(abs_jack, notch=None, vert=None, patch_artist=None, widths=None)
    
    data_miguel = np.array([0.08861533777599271, 0.07272004578265817, 0.05584684596283472, 0.052479996857135802, 0.061460487930597962])
    print(np.mean(data_miguel))
    data_miguel_diff = [data_miguel[0]-data_miguel[1],
                      data_miguel[0]-data_miguel[2],
                      data_miguel[0]-data_miguel[3],
                      data_miguel[0]-data_miguel[4],
                      data_miguel[1]-data_miguel[2],
                      data_miguel[1]-data_miguel[3],
                      data_miguel[1]-data_miguel[4],
                      data_miguel[2]-data_miguel[3],
                      data_miguel[2]-data_miguel[4],
                      data_miguel[3]-data_miguel[4]]
    abs_miguel =  [abs(ele) for ele in data_miguel_diff]
    print(np.mean(abs_miguel))
    print(np.median(abs_miguel))
    q75, q25 = np.percentile(abs_miguel, [75, 25])
    print("q75: %s"%q75)
    print("q25: %s"%q25)
    data_jack_2 = np.array([0.02578766801815441, 0.0376850294818, 0.0685029487457737, 0.048036554032622501, 0.06531330962257842])
    print(np.mean(data_jack_2))
 
    data_jack_2_diff = [data_jack_2[0]-data_jack_2[1],
                      data_jack_2[0]-data_jack_2[2],
                      data_jack_2[0]-data_jack_2[3],
                      data_jack_2[0]-data_jack_2[4],
                      data_jack_2[1]-data_jack_2[2],
                      data_jack_2[1]-data_jack_2[3],
                      data_jack_2[1]-data_jack_2[4],
                      data_jack_2[2]-data_jack_2[3],
                      data_jack_2[2]-data_jack_2[4],
                      data_jack_2[3]-data_jack_2[4]]
    abs_jack_2 =  [abs(ele) for ele in data_jack_2_diff]
    print(np.mean(abs_jack_2))
    print(np.median(abs_jack_2))
    q75, q25 = np.percentile(abs_jack_2, [75, 25])
    print("q75: %s"%q75)
    print("q25: %s"%q25)    
    data = [abs_jack, abs_miguel, abs_jack_2]
    
    matplotlib.pyplot.boxplot(data, notch=None, vert=None, patch_artist=None, widths=None, showmeans=True)
    ax.set_title('Difference in Reconstructed Workspace Volume')
    ax.set_xticklabels(["h1", 'h2', 'h3'])
    ax.set_ylabel('Difference in Volume ($m^3$)')
    matplotlib.pyplot.show()
    
    

