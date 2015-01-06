import logging; logger = logging.getLogger("morse." + __name__)
import morse.core.robot
from morse.helpers.components import add_data, add_property

from morse.core.services import service, async_service, interruptible
from morse.core import status

from morse.core import blenderapi
import bpy
import bge

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
    def getBoundingBox(self):
        #print(blenderapi.scene().objects, "objects")#bpy.data.objects['Male_Base'].show_bounds()
        #print(dir(blenderapi.objectdata('robot')))
        #blenderapi.objectdata('Male_Base').show_wire=False
        #bpy.data.objects['Male_Base'].show_bounds=True
        #print(self.bge_object.parent)
        #print(dir(self.bge_object.parent))
        vertices = []
        vxlist = []
        vylist = []
        vzlist = []
        for child in self.bge_object.childrenRecursive:
            if '_Base' in child.name:
                VSLength = child.meshes[0].getVertexArrayLength(0)

                for vArray in range(0,VSLength):
                    vx,vy,vz = child.meshes[0].getVertex(0,vArray).getXYZ()
                    vxlist.append(vx)
                    vylist.append(vy)
                    vzlist.append(vz)
                #print(min(vxlist),max(vxlist),min(vylist),max(vylist),min(vzlist),max(vzlist))
        return [min(vxlist),max(vxlist),min(vylist),max(vylist),min(vzlist),max(vzlist)]

        #    child.visible=not(child.visible)
        return 1#bpy.data.objects['robot'].bound_box

    @interruptible 
    @async_service
    def set_speed(self, xValue):
        self._speed = xValue
        return 
        
    @service
    def move_forward(self, amount):
        parent = self.bge_object
        parent.applyMovement([amount,0,0],True)
        return amount
        
    def default_action(self):
        """ Main loop of the robot
        """
        vx, vy, vz = 0.0, 0.0, 0.0
        rx, ry, rz = 0.0, 0.0, 0.0

        
        #print(self._speed)        
        vx = self._speed
        
        self.apply_speed('Position', [vx,vy,vz], [rx,ry,rz /2.0])
        self.completed(status.SUCCESS, "Moving Forward")
        
        
        # This is usually not used (responsibility of the actuators
        # and sensors). But you can add here robot-level actions.
        #pass
        
