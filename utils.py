import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import open3d as o3d

def display(V, color='blue'):
    plt.figure(figsize=(8, 8))

    x = V[:, 0]
    y = V[:, 1]

    plt.plot(x, y, color=color, label = "Points")

    plt.axhline(0, color='black', linewidth=1.5, linestyle='-')
    plt.axvline(0, color='black', linewidth=1.5, linestyle='-')

    plt.fill(x, y, color=color, alpha = 0.4)
    plt.gca().set_aspect("equal", adjustable='box')


    plt.show()

#Task 1

def stretch(X, a, b):
    matrix = np.array([[a, 0],
                      [0, b]])
    return X @ matrix, matrix

def shear(X, a, b):
    matrix = np.array([[1, a],
                       [b, 1]])
    return X @ matrix.T, matrix

def reflection(X, a, b):
    matrix = 1 / (a**2 + b**2) * np.array([[a**2-b**2, 2*a*b],
                                          [2*a*b, b**2-a**2]])
    return X @ matrix, matrix

def rotation(X, a):
    matrix = np.array([[np.cos(a), -np.sin(a)], 
                       [np.sin(a), np.cos(a)]])
    return X @ matrix.T, matrix

#task 3

def rotate_xy(X, a):
    matrix = np.array([[np.cos(a), -np.sin(a), 0],
                       [np.sin(a), np.cos(a), 0],
                       [0, 0, 1]])
    return X @ matrix.T, matrix

def rotate_yz(X, a):
    matrix = np.array([[1, 0, 0],
                      [0, np.cos(a), -np.sin(a)],
                      [0, np.sin(a), np.cos(a)]])
    return X @ matrix.T, matrix

def rotate_xz(X, a):
    matrix = np.array([[np.cos(a), 0, -np.sin(a)],
                       [0, 1, 0],
                       [np.sin(a), 0, np.cos(a)]])
    return X @ matrix.T, matrix

def read_off(filename: str):
    with open(filename, 'r') as f:
        if 'OFF' != f.readline().strip():
            raise ValueError('Not a valid OFF header')
        n_verts, n_faces, _ = map(int, f.readline().strip().split())
        verts = [list(map(float, f.readline().strip().split())) for _ in range(n_verts)]

        faces = [list(map(int, f.readline().strip().split()[1:])) for _ in range(n_faces)]

    return np.array(verts), faces

def plot_off(vertices, faces):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    mesh = Poly3DCollection([vertices[face] for face in faces],
                            alpha=0.3, edgecolor='k')
    ax.add_collection3d(mesh)

    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=2, c='b')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.set_aspect('equal')
    
    plt.show()

def visualize_off(vertices, faces):
  mesh = o3d.geometry.TriangleMesh()
  mesh.vertices = o3d.utility.Vector3dVector(
      vertices
  )
  mesh.triangles = o3d.utility.Vector3iVector(
      faces
  )
  mesh.compute_vertex_normals()

  o3d.visualization.draw_geometries([mesh])