import pygame as pg
from matrix_functions import *
import numpy as np
import math

class Camera:
    """
    A 3D camera system that handles movement and rotation in 3D space,
    along with calculating the camera transformation matrix for rendering.
    """

    def __init__(self, render, position):
        """
        Initializes the Camera object.

        Parameters:
        - render: Object that contains rendering settings (WIDTH, HEIGHT).
        - position: Tuple or list of initial (x, y, z) coordinates of the camera.
        """
        self.render = render
        self.position = np.array([*position, 1.0])  # Camera position in homogeneous coordinates

        # Camera orientation vectors (homogeneous)
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

        # Field of view (horizontal and vertical)
        self.h_fov = math.pi / 3  # 60 degrees
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)

        # Clipping planes
        self.near_plane = 0.1
        self.far_plane = 100

        # Movement and rotation speed
        self.moving_speed = 0.3
        self.rotation_speed = 0.015

        # Rotation angles
        self.anglePitch = 0
        self.angleYaw = 0
        self.angleRoll = 0  # Not currently used

    def control(self):
        """
        Handles camera movement and rotation based on keyboard input.
        WASD: Move in local XZ plane
        QE: Move up/down
        Arrow Keys: Rotate camera pitch and yaw
        """
        key = pg.key.get_pressed()

        # Move left/right
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed

        # Move forward/backward
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed

        # Move up/down
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed

        # Rotate camera left/right (yaw)
        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)

        # Rotate camera up/down (pitch)
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)

    def camera_yaw(self, angle):
        """
        Adds yaw (horizontal rotation) to the camera.
        """
        self.angleYaw += angle

    def camera_pitch(self, angle):
        """
        Adds pitch (vertical rotation) to the camera.
        """
        self.anglePitch += angle

    def axiiIdentity(self):
        """
        Resets the orientation vectors to default axis-aligned directions.
        """
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axii(self):
        """
        Updates the forward, right, and up vectors based on the current yaw and pitch.
        """
        # Apply pitch first, then yaw to get correct rotation
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)

        # Reset orientation to base axes before applying rotation
        self.axiiIdentity()

        # Rotate camera axes
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_matrix(self):
        """
        Computes and returns the camera's transformation matrix.
        It combines rotation and translation to move the world relative to the camera.
        """
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()

    def translate_matrix(self):
        """
        Returns the translation matrix that moves the world relative to the camera.
        """
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]  # Move world opposite to camera's position
        ])

    def rotate_matrix(self):
        """
        Returns the rotation matrix constructed from the camera's orientation vectors.
        """
        rx, ry, rz, _ = self.right
        fx, fy, fz, _ = self.forward
        ux, uy, uz, _ = self.up

        # Columns represent the new axes in world space
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [ 0,  0,  0, 1]
        ])
