import math
import numpy as np

def translate(pos):
    """
    Create a translation matrix for a given position vector.
    
    Args:
        pos (tuple or list): A 3-element iterable (tx, ty, tz) representing the translation distances along x, y, and z axes.
    
    Returns:
        np.array: A 4x4 transformation matrix representing the translation.
    """
    tx, ty, tz = pos  # Unpack the translation components
    # Create a 4x4 identity matrix with the translation values in the last row
    return np.array([
        [1, 0, 0, 0],  # No scaling or rotation on the x-axis
        [0, 1, 0, 0],  # No scaling or rotation on the y-axis
        [0, 0, 1, 0],  # No scaling or rotation on the z-axis
        [tx, ty, tz, 1]  # Translation values for x, y, z
    ])

def rotate_x(a):
    """
    Create a rotation matrix around the X-axis.
    
    Args:
        a (float): The angle of rotation in radians.
    
    Returns:
        np.array: A 4x4 transformation matrix representing the rotation around the X-axis.
    """
    # Create the rotation matrix using cosine and sine of the angle 'a'
    return np.array([
        [1, 0,            0,           0],  # X-axis remains unchanged
        [0, math.cos(a),  math.sin(a),  0],  # Rotation in the Y-Z plane
        [0, -math.sin(a), math.cos(a),  0],  # Rotation in the Y-Z plane
        [0, 0,            0,           1]   # Homogeneous coordinate remains 1
    ])

def rotate_y(a):
    """
    Create a rotation matrix around the Y-axis.
    
    Args:
        a (float): The angle of rotation in radians.
    
    Returns:
        np.array: A 4x4 transformation matrix representing the rotation around the Y-axis.
    """
    # Create the rotation matrix using cosine and sine of the angle 'a'
    return np.array([
        [math.cos(a),  0, -math.sin(a), 0],  # Rotation in the X-Z plane
        [0,            1, 0,            0],  # Y-axis remains unchanged
        [math.sin(a),  0, math.cos(a),  0],  # Rotation in the X-Z plane
        [0,            0, 0,            1]   # Homogeneous coordinate remains 1
    ])

def rotate_z(a):
    """
    Create a rotation matrix around the Z-axis.
    
    Args:
        a (float): The angle of rotation in radians.
    
    Returns:
        np.array: A 4x4 transformation matrix representing the rotation around the Z-axis.
    """
    # Create the rotation matrix using cosine and sine of the angle 'a'
    return np.array([
        [math.cos(a),  math.sin(a), 0, 0],  # Rotation in the X-Y plane
        [-math.sin(a), math.cos(a), 0, 0],  # Rotation in the X-Y plane
        [0,            0,           1, 0],  # Z-axis remains unchanged
        [0,            0,           0, 1]   # Homogeneous coordinate remains 1
    ])

def scale(n):
    """
    Create a scaling matrix with a uniform scale factor.
    
    Args:
        n (float): The uniform scale factor for x, y, and z axes.
    
    Returns:
        np.array: A 4x4 transformation matrix representing the scaling.
    """
    # Create a diagonal matrix with the scale factor 'n' on the diagonal (except for the homogeneous coordinate)
    return np.array([
        [n, 0, 0, 0],  # Scale x-axis
        [0, n, 0, 0],  # Scale y-axis
        [0, 0, n, 0],  # Scale z-axis
        [0, 0, 0, 1]   # Homogeneous coordinate remains 1
    ])
