import pygame as pg
from matrix_functions import *
from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b):
    """
    Check if any element in the array is equal to 'a' or 'b'.
    
    Parameters:
        arr (array): The array to check.
        a (numeric): The first value to compare against.
        b (numeric): The second value to compare against.
    
    Returns:
        bool: True if any element in arr is equal to a or b, otherwise False.
    """
    return np.any((arr == a) | (arr == b))


class Object3D:
    """
    A class representing a 3D object with vertices and faces,
    capable of undergoing various transformations and being projected
    onto a 2D screen for rendering with pygame.
    """
    def __init__(self, render):
    # def __init__(self, render, vertices, faces):
        """
        Initialize the 3D object.
        
        Parameters:
            render: The rendering context which contains camera, projection matrices, screen, etc.
            vertices: A list or array of vertices representing the object's points.
            faces: A list of faces, where each face is defined by indices into the vertices array.
        """
        self.render = render
        self.vertices = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1), (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)])
        # self.vertices = np.array(vertices)  # Convert vertices to a numpy array for matrix operations
        self.faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)])
        # self.faces = faces

        # Apply a small translation to ensure object is not exactly at the origin
        self.translate([0.0001, 0.0001, 0.0001])

        # Initialize font for any labels that might be drawn on the object
        self.font = pg.font.SysFont('Arial', 30, bold=True)

        # Pair each face with an orange color by default
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]

        # Flags for object behavior
        self.movement_flag = True  # Determines if object should move (rotate)
        self.draw_vertices = False  # Determines if vertices should be drawn as circles
        self.label = ''  # Label text for each face if provided

    def draw(self):
        """
        Render the object by projecting it onto the screen and applying movement.
        """
        self.screen_projection()  # Project 3D vertices onto the 2D screen
        self.movement()  # Apply movement (rotation) if enabled

    def movement(self):
        """
        Apply rotational movement to the object if movement_flag is True.
        """
        if self.movement_flag:
            # Rotate around the y-axis based on the elapsed time
            # Note: pg.time.get_ticks() returns time in milliseconds
            self.rotate_y(-(pg.time.get_ticks() % 0.005))

    def screen_projection(self):
        """
        Project the 3D vertices of the object onto the 2D screen and render the faces.
        """
        # Apply the camera transformation to the vertices
        vertices = self.vertices @ self.render.camera.camera_matrix()
        # Apply the projection matrix
        vertices = vertices @ self.render.projection.projection_matrix
        # Perform perspective division to normalize coordinates
        vertices /= vertices[:, -1].reshape(-1, 1)
        # Discard vertices that are out of the normalized device coordinate bounds
        vertices[(vertices > 2) | (vertices < -2)] = 0
        # Convert normalized coordinates to screen coordinates
        vertices = vertices @ self.render.projection.to_screen_matrix
        # Only keep the x and y coordinates for 2D rendering
        vertices = vertices[:, :2]

        # Draw each face of the object
        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            # Get the 2D points that form the polygon for the current face
            polygon = vertices[face]
            # Check if the polygon is within the screen bounds before drawing
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, color, polygon, 1)
                # Render and draw the label on the face if a label exists
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, polygon[-1])

        # Optionally draw each vertex as a small circle
        if self.draw_vertices:
            for vertex in vertices:
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

    def translate(self, pos):
        """
        Translate the object by the given position vector.
        
        Parameters:
            pos (list or tuple): The translation vector [dx, dy, dz].
        """
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):
        """
        Scale the object by the given factor.
        
        Parameters:
            scale_to (numeric or list/tuple): The scale factor(s) to apply.
        """
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        """
        Rotate the object around the x-axis by the given angle.
        
        Parameters:
            angle (float): The rotation angle in radians.
        """
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        """
        Rotate the object around the y-axis by the given angle.
        
        Parameters:
            angle (float): The rotation angle in radians.
        """
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        """
        Rotate the object around the z-axis by the given angle.
        
        Parameters:
            angle (float): The rotation angle in radians.
        """
        self.vertices = self.vertices @ rotate_z(angle)


class Axes(Object3D):
    """
    A subclass of Object3D representing the 3D coordinate axes (X, Y, Z).
    """
    def __init__(self, render):
        """
        Initialize the Axes object with predefined vertices, faces, and colors.
        
        Parameters:
            render: The rendering context.
        """
        # Initialize base Object3D with the render context
        super().__init__(render)
        # Define vertices for the origin and points along the axes
        self.vertices = np.array([
            (0, 0, 0, 1),  # Origin
            (1, 0, 0, 1),  # X-axis
            (0, 1, 0, 1),  # Y-axis
            (0, 0, 1, 1)   # Z-axis
        ])
        # Define faces as line segments connecting the origin to each axis point
        self.faces = np.array([
            (0, 1),  # Line for X-axis
            (0, 2),  # Line for Y-axis
            (0, 3)   # Line for Z-axis
        ])
        # Define colors for each axis: red for X, green for Y, blue for Z
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        # Associate each axis (face) with its corresponding color
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False  # Do not draw individual vertices for the axes
        self.label = 'XYZ'  # Label for the axes (each character corresponds to an axis)
        