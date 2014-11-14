import logging; logger = logging.getLogger("morse." + __name__)
import morse.core.robot
from morse.helpers.components import add_data, add_property

from morse.core.services import service, async_service, interruptible
class Manny(morse.core.robot.Robot):
    """ 
    Class definition for the Manny robot.
    """

    _name = 'Manny robot'

    def __init__(self, obj, parent=None):
        """ Constructor method

        Receives the reference to the Blender object.
        Optionally it gets the name of the object's parent,
        but that information is not currently used for a robot.
        """
        add_property('_speed', 0.0, 'Speed', 'float',
                    "movement speed of the robot in m/s")

        self._speed = 0.0
        logger.info('%s initialization' % obj.name)
        morse.core.robot.Robot.__init__(self, obj, parent)

        # Do here robot specific initializations
        logger.info('Component initialized')
    
    @service
    def set_speed(self, xValue):
        self._speed = xValue
        return 
        
    @service
    def move(self, amount):
        parent = self.bge_object
        parent.applyMovement([amount,0,0],True)
        return
        
    def default_action(self):
        """ Main loop of the robot
        """
        vx, vy, vz = 0.0, 0.0, 0.0
        rx, ry, rz = 0.0, 0.0, 0.0

        
        #print(self._speed)        
        vx = self._speed
        
        self.apply_speed('Position', [vx,vy,vz], [rx,ry,rz /2.0])
        
        # This is usually not used (responsibility of the actuators
        # and sensors). But you can add here robot-level actions.
        #pass
        
