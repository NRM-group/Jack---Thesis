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
    X_raw = np.genfromtxt(r'/home/medrobotics/jack_ws/src/mrn_movo/data/test_jack_2.csv', delimiter=',')
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
    
    
    visualise_pcl(X_filt)

    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(X_filt)

    
    
    alpha = 0.3
    radii = [0.005, 0.01, 0.02, 0.04]
    print(f"alpha={alpha:.3f}")
    
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
    mesh.compute_vertex_normals()
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[0, 0, 0])
    o3d.visualization.draw_geometries([mesh, mesh_frame], mesh_show_back_face=True)
    volume = o3d.geometry.TriangleMesh.get_volume(mesh)
    print(volume)

    
  
    
    

