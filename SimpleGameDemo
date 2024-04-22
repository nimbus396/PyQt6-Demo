import sys
import random

from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPainter, QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    """
    Class variable which control the screen layout and objects
    """
    __SCREEN_WIDTH = 640
    __SCREEN_HEIGHT = 480
    __HALF_HEIGHT = int(__SCREEN_HEIGHT * .66)
    __LINE_START = __HALF_HEIGHT
    __NUM_STARS = 250
    __NUM_COLORS = 255 ** 3
    __BLIT_TIME = 50
    __OFFSETS_0 = [1, 2, 3, 5,  8, 13, 21, 27, 34,  55,  89]
    __OFFSETS_1 = [2, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199]
    __OFFSETS_2 = [3, 4, 5, 9, 14, 23, 37, 60, 97, 157, 200]
    __LINE_COLORS = [Qt.GlobalColor.cyan, Qt.GlobalColor.white]
    __CURRENT_LINE_SET = 2
    __SHIP_WIDTH = 32
    __SHIP_HEIGHT = 32

    def __init__(self):
        """
        Intialize the class and setup the objects for the class.
        Objects: label, screen, painter
        label: central widget for the main window
        screen: QPixmap object which will be drawn by painter object
        painter: QPainter object for drawing
        """
        super().__init__()
        self.points=[]
        self.shipX = (MainWindow.__SCREEN_WIDTH/2)-(MainWindow.__SHIP_WIDTH/2)
        self.shipY = MainWindow.__SCREEN_HEIGHT-MainWindow.__SHIP_HEIGHT

        # Set the locations for the stars
        for i in range(0,MainWindow.__NUM_STARS):
            self.points.append(QPoint(random.randint(0, MainWindow.__SCREEN_WIDTH), random.randint(0, MainWindow.__HALF_HEIGHT)))

        # We will use a label as the screen and fill it with the color black.
        # This will be our screen to draw objects. In order to do that, we
        # need to setup a Pixel map object to draw.
        self.label = QLabel()
        self.screen = QPixmap(MainWindow.__SCREEN_WIDTH, MainWindow.__SCREEN_HEIGHT)
        self.screen.fill(Qt.GlobalColor.black)
        # In order to draw on the pixel map, we need a painter object
        # attached as our canvas.
        self.painter = QPainter(self.screen)
        self.label.setPixmap(self.screen)

        # Setup the images. One is the ship, the other is a blank tile
        self.shipImage = QImage("r.png").scaled(MainWindow.__SHIP_WIDTH,MainWindow.__SHIP_HEIGHT,Qt.AspectRatioMode.IgnoreAspectRatio)
        self.shipBlank = QImage("b.png").scaled(MainWindow.__SHIP_WIDTH,MainWindow.__SHIP_HEIGHT,Qt.AspectRatioMode.IgnoreAspectRatio)

        # Set the main window widget to the drawable screen
        self.setCentralWidget(self.label)

        # We have to draw the stars or these will just appear
        # one second after the screen is drawn.
        self.draw_stars()

        # Instead of an event loop for changing stars and lines
        # we will use a QTimer object. One for the stars, 
        # one for the lines and one for the ship. We do this because
        # each function has different timings. We could count clocks
        # but, these are built for the job.

        # Stars blink every 1 second
        self.starTimer=QTimer()
        self.starTimer.setInterval(1000)
        self.starTimer.timeout.connect(self.draw_stars)
        self.starTimer.start()

        # __BLIT_TIME is dynamic
        self.lineTimer=QTimer()
        self.lineTimer.timeout.connect(self.draw_lines)
        self.lineTimer.setInterval(MainWindow.__BLIT_TIME)
        self.lineTimer.start()

        # Repaint the ship after every one ms
        self.shipTimer=QTimer()
        self.shipTimer.timeout.connect(self.draw_ship)
        self.shipTimer.setInterval(1)
        self.shipTimer.start()
        self.draw_ship()
    """
        Function: draw_stars
        Parameters: none
        Return: none

        Description: The stars are fixed points and are
                     set when the function is initialized.
                     draw_stars() will cause the colors to
                     change.
    """
    def draw_stars(self):

        # Tell the painter we are starting to draw on the canvas
        self.painter.begin(self.screen)

        # For each star, chose a random color
        # and set the point to the random color.
        for i in range(0, MainWindow.__NUM_STARS):
             c=random.randint(0,MainWindow.__NUM_COLORS)
             self.painter.setPen(c)
             self.painter.pen().setWidth(2)
             self.painter.drawPoint(self.points[i])
        # Tell the painter we are done.
        # We don't need to update the pixmap here. We
        # will let the draw_lines() function perform
        # the redraw to our canvas.
        self.painter.end()

    """
        Function: draw_lines
        Parameters: none
        Return: none
        
        Description: This will rotate through a set of offsets.
                     We could calculate these on the fly but,
                     that cost time. Using presets saves us
                     some processing time.
    """
    def draw_lines(self):
        # Tell the painter we want to draw on the canvas
        self.painter.begin(self.screen)

        # We don't want to redraw the whole screen every time.
        # We just want to repaint the bottom. Set the pen to black
        # and clear the bottom.
        #self.painter.setPen(Qt.GlobalColor.black)
        #for i in range(MainWindow.__HALF_HEIGHT, MainWindow.__SCREEN_HEIGHT):
            #self.painter.drawLine(0, i, MainWindow.__SCREEN_WIDTH,i)
        self.painter.setPen(Qt.GlobalColor.black)
        if MainWindow.__CURRENT_LINE_SET == 2:
            lineset = MainWindow.__OFFSETS_0.copy()
        elif MainWindow.__CURRENT_LINE_SET == 1:
            lineset = MainWindow.__OFFSETS_2.copy()
        else:
            lineset = MainWindow.__OFFSETS_1.copy()
        # Draw the lines based on the current line set
        for i in range(0, len(MainWindow.__OFFSETS_0)):
            self.painter.drawLine(0, MainWindow.__LINE_START + lineset[i], MainWindow.__SCREEN_WIDTH,
                             MainWindow.__LINE_START + lineset[i])
        # Select the next pre-defined line set based on the
        # current line set.
        if MainWindow.__CURRENT_LINE_SET == 2:
            lineset = MainWindow.__OFFSETS_2.copy()
            MainWindow.__CURRENT_LINE_SET = 1
        elif MainWindow.__CURRENT_LINE_SET == 1:
            lineset = MainWindow.__OFFSETS_1.copy()
            MainWindow.__CURRENT_LINE_SET = 0
        else:
            lineset = MainWindow.__OFFSETS_0.copy()
            MainWindow.__CURRENT_LINE_SET = 2

        # Set the line color to cyan. In theory, for a game,
        # for each level, you could have a different color
        self.painter.setPen(Qt.GlobalColor.cyan)
        # Draw the lines based on the current line set
        for i in range(0, len(MainWindow.__OFFSETS_0)):
            self.painter.drawLine(0, MainWindow.__LINE_START + lineset[i], MainWindow.__SCREEN_WIDTH,
                             MainWindow.__LINE_START + lineset[i])
        #self.draw_ship()
        # Tell the painter to stop drawing
        self.painter.end()

    def draw_ship(self):
        self.painter.begin(self.screen)
        self.painter.drawImage(self.shipX, self.shipY, self.shipImage)
        self.painter.end()
        # Update the canvas
        self.label.setPixmap(self.screen)
    """
        Function: closeEvent()
        Parameter: event - The event will be captured but not used
        Return: none
        
        Description:
        This is an override to the default handling of the close event
        for a window. Stop all timers and close the window.
    """
    def closeEvent(self, event):
        self.starTimer.stop()
        self.lineTimer.stop()
        self.shipTimer.stop()
        self.close()

    """
        Function: mousePressEvent()
        Parameter: event - The event will be captured but not used
        
        Description: This is an override of the default handling of a
                     mouse press. It will increase, reset or decrease
                     the line speed. This is for testing purpose and
                     would not be in production.
    """
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            MainWindow.__BLIT_TIME += 1
        elif event.button() == Qt.MouseButton.MiddleButton:
            MainWindow.__BLIT_TIME = 100
        elif event.button() == Qt.MouseButton.RightButton:
            MainWindow.__BLIT_TIME -= 1
        self.lineTimer.setInterval(MainWindow.__BLIT_TIME)
        print(MainWindow.__BLIT_TIME)

    def keyReleaseEvent(self, event):
        self.painter.begin(self.screen)
        self.painter.drawImage(self.shipX, self.shipY, self.shipBlank)
        self.painter.end()
        k=event.key()
        if k == Qt.Key.Key_Up:
            self.shipY -= 5
        elif k == Qt.Key.Key_Down:
            self.shipY += 5
        elif k == Qt.Key.Key_Left:
            self.shipX -=5
        elif k == Qt.Key.Key_Right:
            self.shipX += 5

        if self.shipX > MainWindow.__SCREEN_WIDTH-MainWindow.__SHIP_WIDTH:
            self.shipX = MainWindow.__SCREEN_WIDTH-MainWindow.__SHIP_WIDTH
        elif self.shipX < 0:
            self.shipX = 0
        elif self.shipY < MainWindow.__HALF_HEIGHT:
            self.shipY = MainWindow.__HALF_HEIGHT
        elif self.shipY > MainWindow.__SCREEN_HEIGHT - MainWindow.__SHIP_HEIGHT:
            self.shipY = MainWindow.__SCREEN_HEIGHT - MainWindow.__SHIP_HEIGHT

# Set up the application and call the main window.
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
