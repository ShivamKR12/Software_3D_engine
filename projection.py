import math
import numpy as np

class Projection:
    """
    Projection class responsible for calculating the projection and screen transformation matrices
    based on the camera properties in the provided render object.

    Attributes:
        projection_matrix (np.array): The projection matrix for transforming 3D coordinates into clip space.
        to_screen_matrix (np.array): The transformation matrix to convert clip space coordinates to screen space.
    """

    def __init__(self, render):
        """
        Initializes the Projection object by computing the projection and screen matrices using the camera parameters.

        Args:
            render: An object containing camera settings and screen dimensions.
                    It should have a 'camera' attribute with properties: near_plane, far_plane, h_fov, and v_fov.
                    It should also have 'H_WIDTH' and 'H_HEIGHT' attributes for half the screen width and height.
        """
        # Retrieve near and far plane distances from the camera
        NEAR = render.camera.near_plane
        FAR = render.camera.far_plane
        
        # Calculate right and left boundaries based on horizontal field of view (FOV)
        RIGHT = math.tan(render.camera.h_fov / 2)
        LEFT = -RIGHT

        # Calculate top and bottom boundaries based on vertical field of view (FOV)
        TOP = math.tan(render.camera.v_fov / 2)
        BOTTOM = -TOP

        # Compute elements for the projection matrix
        m00 = 2 / (RIGHT - LEFT)       # Scale factor for the x-axis
        m11 = 2 / (TOP - BOTTOM)         # Scale factor for the y-axis
        m22 = (FAR + NEAR) / (FAR - NEAR)  # Depth scale factor
        m32 = -2 * NEAR * FAR / (FAR - NEAR)  # Depth translation component

        # Create the projection matrix that converts view space to clip space
        self.projection_matrix = np.array([
            [m00, 0,   0,   0],
            [0,   m11, 0,   0],
            [0,   0,   m22, 1],
            [0,   0,   m32, 0]
        ])

        # Retrieve half the screen width and height for screen space transformation
        HW, HH = render.H_WIDTH, render.H_HEIGHT

        # Create the screen transformation matrix that maps clip space coordinates to screen space
        self.to_screen_matrix = np.array([
            [HW,  0,   0, 0],
            [0,  -HH,  0, 0],
            [0,   0,   1, 0],
            [HW,  HH,  0, 1]
        ])
