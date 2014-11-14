import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.actuator

from morse.core import mathutils
#from morse.builder import Actuator, Armature

from morse.core.services import service, async_service, interruptible
from morse.core import status
from morse.helpers.components import add_data, add_property

class Torso(morse.core.actuator.Actuator):
    """Write here the general documentation of your actuator.
    It will appear in the generated online documentation.
    """
    _name = "Torso"
    _short_desc = "Torso movement"

    # define here the data fields required by your actuator
    # format is: field name, initial value, type, description
    add_data('counter', 0, 'int', 'A dummy counter, for testing purposes')

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.actuator.Actuator.__init__(self, obj, parent)
        #self.properties(classpath = "ACT_v1.actuators.Manny.Manny")
        #self.add_meshes(['Armature'])
        # Do here actuator specific initializations
        
        self._segments = []
        segment = self.bge_object.children[0]
        
        for i in range(1):
            self._segments.append(segment)
            try:
                segment = segment.children[0]
            except IndexError:
                break
        logger.info("Arm segment list:" +  repr(self._segments))
        logger.info(repr(dir(self.bge_object)) + " dir")
        self._rib = None
        logger.info('self ' + self.bge_object.name)
        for child in self.bge_object.channels:
            if 'ribs' in child.name:
                self._rib = child
                logger.info('Ribs found.')
            logger.info('Child: ' + child.name + ' found.')  
        for child in self.bge_object.children:
            if 'ube' in child.name:
                self._cube = child
                
        #logger.info(repr(dir(self._rib.pose_head)))
        #self.rotate(self._rib, (0.0,0.0,0.5), 3)
        #self._rib.pose_head.rotate(mathutils.Euler([1.0,1,1.5]))
        #logger.info(help(self._rib.joint_rotation))
        #logger.info(repr(dir(self.bge_object)))
        #self._rib.rotation_euler = (0.0,0.0,0.5)
        #self._rib.joint_rotation[2] = 0.5
        #self.set_rotation(1.5)
        #self._rib.joint_rotation.rotate(mathutils.Euler([0.5,0.5,0.5]))        
        #logger.info(self._rib.rotation_euler)
        #self._cube.applyRotation([0.0,0.0,0.5],True)
        #self._rib.rotation_euler = (1,1,1)
        self._target_count = 0 # dummy internal variable, for testing purposes

        logger.info('Component initialized')
    
    @service
    def set_rotation(self, rotation):
        tmp = self._rib.joint_rotation
        tmp[1] = tmp[1] + rotation
        self._rib.joint_rotation = tmp 
        
        
    @service
    def get_counter(self):
        """ This is a sample service.

        Simply returns the value of the internal counter.

        You can access it as a RPC service from clients.
        """
        logger.info("%s counter is %s" % (self.name, self.local_data['counter']))

        return self.local_data['counter']

    @interruptible
    @async_service
    def async_test(self, value):
        """ This is a sample asynchronous service.

        Returns when the internal counter reaches ``value``.

        You can access it as a RPC service from clients.
        """
        self._target_count = value

    def default_action(self):
        """ Main loop of the actuator.

        Implements the component behaviour
        """
        
        #self.set_rotation(0.5)
        #self.set_rotation(0)
        # check if we have an on-going asynchronous tasks...
        if self._target_count and self.local_data['counter'] > self._target_count:
            self.completed(status.SUCCESS, self.local_data['counter'])

        # implement here the behaviour of your actuator
        self.local_data['counter'] += 1
        
        self.bge_object.update()
