import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.actuator

from morse.core import mathutils
#from morse.builder import Actuator, Armature

from morse.core.services import service, async_service, interruptible
from morse.core import status
from morse.helpers.components import add_data, add_property


import math

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
            if 'arm_upper.L' in child.name:
                self._leftUpperArm = child
                logger.info('LeftUpperArm found')
            if 'arm_upper.R' in child.name:
                self._rightUpperArm = child
                logger.info('RightUpperArm found')
            if 'shoulder.L' in child.name:
                self._leftShoulder = child
            if 'shoulder.R' in child.name:
                self._rightShoulder = child


            logger.info('Child: ' + child.name + ' found.')
 
        #self._rib.rotation_euler = (1,1,1)
        self._target_count = 0 # dummy internal variable, for testing purposes
        self._target_count2 = 0

        logger.info('Component initialized')
        
    def _get_revolute(self, joint):
        """ Checks a given revolute joint name exist in the armature, and
        returns it.
        """
        channel, is_prismatic = self._get_joint(joint)

        if is_prismatic:
            msg = "Joint %s is not a revolute joint! Can not set the rotation" % joint
            raise MorseRPCInvokationError(msg)

        return channel
    
#    @service
#    def set_rotation(self, rotation):
#        tmp = self._rib.joint_rotation
#        tmp[1] = tmp[1] + rotation
#        self._rib.joint_rotation = tmp 
    @service
    def set_rotation(self, joint, axis, radians):
        '''Access a joint by name and rotate it by radians on axis (0,1,2)
            ribs,1-> shoulder rotation
            shoulder.L,2 -> sub/shoulder compression/expansion (left)
            shoulder.R,0 -> sub/shoulder compression/expansion (right)
            Fix why different axes?'''
        channel = self._get_revolute(joint)
        
        tmp = channel.joint_rotation
        tmp[axis] = radians
        channel.joint_rotation = tmp 
        return   


    @service
    def lower_arms(self):
        self.set_rotation('arm_upper.L',0,math.radians(-40))
        self.set_rotation('arm_upper.R',0,math.radians(40))
        return
    
    @service
    def shoulder_rotate(self):
        print(self._rightShoulder.joint_rotation)
        self._rightShoulder.joint_rotation[2] = self._rightShoulder.joint_rotation[2] - 0.1    
        print(self._rightShoulder.joint_rotation)
        return


    def _get_joint(self, joint):
        """ Checks a given joint name exist in the armature,
        and returns it as a tuple (Blender channel, is_prismatic?)

        If the joint does not exist, throw an exception.
        """
        armature = self.bge_object

        if joint not in [c.name for c in armature.channels]:
            msg = "Joint <%s> does not exist in armature %s" % (joint, armature.name)
            raise MorseRPCInvokationError(msg)

        channel = armature.channels[joint]

        if self._is_prismatic(channel):
            return channel, True
        else:
            return channel, False
   
    def _is_prismatic(self, channel):
        """
        Important: The detection of prismatic joint relies solely on a
        non-zero value for the IK parameter 'ik_stretch'.
        """
        return True if channel.ik_stretch else False
    
    def _get_joint_value(self, joint):
        """
        Returns the *value* of a given joint, either:
        - its absolute rotation in radian along its rotation axis, or
        - it absolute translation in meters along its translation axis.

        Throws an exception if the joint does not exist.

        :param joint: the name of the joint in the armature.
        """
        channel, is_prismatic = self._get_joint(joint)

        # Retrieve the motion axis
        axis_index = next(i for i, j in enumerate(self.find_dof(channel)) if j)

        if is_prismatic:
            return channel.pose_head[2] #The 'Z' value
        else: # revolute joint
            return channel.joint_rotation[axis_index]
    @service
    def get_counter(self):
        """ This is a sample service.

        Simply returns the value of the internal counter.

        You can access it as a RPC service from clients.
        """
        logger.info("%s counter is %s" % (self.name, self.local_data['counter']))

        return self.local_data['counter']

    #@interruptible
    @async_service
    def async_test2(self,value):
        self._target_count2 = value
    
    
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

        self.completed(status.SUCCESS, 'a')

        # implement here the behaviour of your actuator
        self.local_data['counter'] += 1
        
        self.bge_object.update()
