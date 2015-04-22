import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.actuator

from morse.core.services import service, async_service, interruptible
from morse.core import status
from morse.helpers.components import add_data, add_property

class MannequinTorso(morse.core.actuator.Actuator):
    """Write here the general documentation of your actuator.
    It will appear in the generated online documentation.
    """
    _name = "Mannequintorso"
    _short_desc = "Just the body portion of the overall robot."

    # define here the data fields required by your actuator
    # format is: field name, initial value, type, description
    add_data('counter', 0, 'int', 'A dummy counter, for testing purposes')

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.actuator.Actuator.__init__(self, obj, parent)

        # Do here actuator specific initializations

        self._target_count = 0 # dummy internal variable, for testing purposes

        logger.info('Component initialized')
    
    def _is_prismatic(self, channel):
        """
        Important: The detection of prismatic joint relies solely on a
        non-zero value for the IK parameter 'ik_stretch'.
        """
        return True if channel.ik_stretch else False
    
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
    def _get_revolute(self, joint):
        """ Checks a given revolute joint name exist in the armature, and
        returns it.
        """
        channel, is_prismatic = self._get_joint(joint)

        if is_prismatic:
            msg = "Joint %s is not a revolute joint! Can not set the rotation" % joint
            raise MorseRPCInvokationError(msg)

        return channel
    @service
    def set_rotation(self, joint, axis, radians):
        '''Access a joint by name and rotate it by radians on axis (0,1,2)
            ribs,1-> shoulder rotation
            shoulder.L,2 -> sub/shoulder compression/expansion (left)
            shoulder.R,0 -> sub/shoulder compression/expansion (right)
            Fix why different axes?'''
        channel = self._get_revolute(joint)
        tmp = channel.joint_rotation
        print("HERE MOTHER FUCKER",tmp)
        tmp[axis] = radians
        
        channel.joint_rotation = tmp 
        print("HERE MOTHER FUCKER2",channel.joint_rotation)
        return radians
   
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

        # check if we have an on-going asynchronous tasks...
        #if self._target_count and self.local_data['counter'] > self._target_count:
        #    self.completed(status.SUCCESS, self.local_data['counter'])

        # implement here the behaviour of your actuator
        #self.local_data['counter'] += 1

        self.bge_object.update()
