#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <ACT_v1> environment

Feel free to edit this template as you like!
"""
import pdb

import bpy
import math
from ACT_v1.builder.robots import Manny
#from ACT_v1.builder.actuators import Mannyactuator
from ACT_v1.builder.sensors.Collision import Collision as LocalCollision
#from ACT_v1.builder.actuators import Torso

from morse.builder import *
#from ACT_v1.builder.actuators import Draw1
#from ACT_v1.builder.sensors import SemanticCamera#Geometriccamerav1
from morse.core.morse_time import TimeStrategies

bpymorse.set_speed(10, 1, 1)
xxx = bpymorse.set_speed
# Add the MORSE mascott, MORSY.
# Out-the-box available robots are listed here:
# http://www.openrobots.org/morse/doc/stable/components_library.html
#
# 'morse add robot <name> ACT_v1' can help you to build custom robots.
#robot = Morsy()
##robot = Human()
##robot.use_world_camera()
##robot.disable_keyboard_control()


#going to try manny
robot = Manny()


# The list of the main methods to manipulate your components
# is here: http://www.openrobots.org/morse/doc/stable/user/builder_overview.html
robot.translate(-1.0, 0.0, 0.0)


armature = Armature(model_name='ACT_v1/actuators/Torso.blend', armature_name='Armature')

armature.properties(classpath = "ACT_v1.actuators.Torso.Torso")
armature.translate(0,0,-1.2)
armature.rotate(z=math.radians(90))


#armature.rotate(0.0,0.0,0.0)
#armature.rotate(0,0,math.radians(90))
#armature.create_ik_targets(['shoulder.L'])
#armature.create_ik_targets(['arm_lower.L'])
#ik_target.robot.armature.shoulder.L
#ik_target.robot.armature.shoulder.R
#armature.place_IK_targets('ik_target.robot.armature.shoulder.L', [0.04,0.04,0.53],None,False)


#collision = Collision()
#collision.properites(collision_property="obstacle")
#armature.append(collision)

#armproximity = Proximity()
#armproximity.properties(Track = 'obstacle')
#armproximity.properties(Range=5.0)
#armproximity.add_stream('socket')
#armature.append(armproximity)
#armcollision = Collision()
#armcollision.properties(collision_property="obstacle")
#armcollision.add_stream('socket')

#armature.append(armcollision)


robot.append(armature)
armature.add_service('socket')



#collision = Collision()
#collision.properties(collision_property="obstacle")
#robot.append(collision)
#logger.info(dir(collision))
#robot.properties(obstacle=1)
#armature = Armature(model_name="ACT_v1/robots/Manny_armature.blend", armature_name='ribs')
#robot.append(armature)

#armature.rotate("ribs",0.5).result()

#torso = Mannyactuator()
#robot.append(torso)

#torso = Torso()

#robot.append(torso)

#Make a Draw1
#draw1 = Draw1()
#robot.append(draw1)



# Add a motion controller
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
#
# 'morse add actuator <name> ACT_v1' can help you with the creation of a custom
# actuator.


#Geometric camera
GeometricCamerav1 = SemanticCamera()

GeometricCamerav1.translate(x=0.11,y=-0.0,z=0.52)
GeometricCamerav1.properties(Object=False)
GeometricCamerav1.properties(cam_width=2048,cam_height=2048)
GeometricCamerav1.properties(cam_focal=18)
GeometricCamerav1.rotate(math.radians(00),0,0)
robot.append(GeometricCamerav1)
#geometric1.add_stream('socket')

#Face the wall
robot.rotate(z=math.radians(90))

motion = MotionVW()
robot.append(motion)
motion.add_stream('socket')

# Add a keyboard controller to move the robot with arrow keys.
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(ControlType = 'Position')

# Add a pose sensor that exports the current location and orientation
# of the robot in the world frame
# Check here the other available actuators:
# http://www.openrobots.org/morse/doc/stable/components_library.html#sensors
#
# 'morse add sensor <name> ACT_v1' can help you with the creation of a custom
# sensor.
pose = Pose()
robot.append(pose)
#pose.translate(z=50)

robot.add_service('socket')


# To ease development and debugging, we add a socket interface to our robot.
#
# Check here: http://www.openrobots.org/morse/doc/stable/user/integration.html 
# the other available interfaces (like ROS, YARP...)
robot.add_default_interface('socket')


# set 'fastmode' to True to switch to wireframe mode
env = Environment('../projects/ACT_v1/my_house.blend')

env.set_camera_location([10.0, -10.0, 10.0])
env.set_camera_rotation([1.05, 0, 0.78])
env.select_display_camera(GeometricCamerav1)
#pdb.set_trace()
env.set_time_strategy(TimeStrategies.FixedSimulationStepExternalTrigger)
env.show_framerate(True)
#env.show_physics(True)


