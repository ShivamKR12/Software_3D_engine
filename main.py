from object_3d import *  # Import 3D object-related classes and functions
from camera import *       # Import camera-related classes and functions
from projection import *   # Import projection-related classes and functions
import pygame as pg      # Import pygame for rendering and event handling
import math              # Import math for mathematical operations

class SoftwareRender:
    """
    A software renderer that sets up a 3D scene with camera, projection, and 3D objects.
    Uses pygame for window creation and event handling.
    """
    def __init__(self):
        """
        Initializes the rendering environment, sets display parameters,
        creates objects, and configures the clock for framerate control.
        """
        pg.init()  # Initialize all imported pygame modules
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900  # Screen resolution
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2  # Half-dimensions for centering
        self.FPS = 60  # Frames per second
        self.screen = pg.display.set_mode(self.RES)  # Create the display surface
        self.clock = pg.time.Clock()  # Clock to manage framerate
        self.create_objects()  # Set up camera, projection, and 3D objects

    def create_objects(self):
        """
        Create and initialize the camera, projection, and 3D object from file.
        """
        # Initialize the camera with a starting position
        self.camera = Camera(self, [0.5, 1, -4])
        # self.camera = Camera(self, [-5, 6, -55])
        # Set up the projection matrix using camera parameters
        self.projection = Projection(self)
        # Load a 3D object from an OBJ file
        # self.object = self.get_object_from_file('resources/t_34_obj.obj')
        # Rotate the object around the Y-axis by -45 degrees for better orientation
        # self.object.rotate_y(-math.pi / 4)
        
        self.object = Object3D(self)
        self.object.translate([0.2, 0.4, 0.2])
        self.axes = Axes(self)
        self.axes.translate([0.7, 0.9, 0.7])
        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False
        self.world_axes.scale(2.5)
        self.world_axes.translate([0.0001, 0.0001, 0.0001])

    def get_object_from_file(self, filename):
        """
        Reads a 3D object's vertex and face data from a file and creates an Object3D.

        Args:
            filename (str): Path to the 3D object file in OBJ format.

        Returns:
            Object3D: An instance of Object3D created using the parsed vertex and face data.
        """
        vertex, faces = [], []  # Lists to store vertex and face information
        with open(filename) as f:
            for line in f:
                # Process vertex data lines (starting with 'v ')
                if line.startswith('v '):
                    # Convert each component to float and add homogeneous coordinate (1)
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                # Process face data lines (starting with 'f')
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    # Convert vertex indices (OBJ indices start at 1, so subtract 1)
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        # Create and return the Object3D using the collected vertex and face data
        return Object3D(self, vertex, faces)

    def draw(self):
        """
        Clears the screen and draws the 3D object.
        """
        # Fill the screen with a dark slate gray background color
        self.screen.fill(pg.Color('darkslategray'))
        # Render the 3D object to the screen
        self.object.draw()
        self.world_axes.draw()
        self.axes.draw()

    def run(self):
        """
        Main loop of the renderer. Handles drawing, event processing, and frame rate control.
        """
        while True:
            self.draw()  # Draw the current frame
            self.camera.control()  # Update camera based on user input
            # Check for quit events and exit if found
            key = pg.key.get_pressed()
            [exit() for i in pg.event.get() if i.type == pg.QUIT or key[pg.K_ESCAPE]]
            # Set the window title to the current FPS
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()  # Update the full display surface to the screen
            self.clock.tick(self.FPS)  # Maintain the target frames per second

if __name__ == '__main__':
    # Instantiate the SoftwareRender class and start the rendering loop
    app = SoftwareRender()
    app.run()
