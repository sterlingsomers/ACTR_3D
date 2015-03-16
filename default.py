#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <ACT_v1> environment

Feel free to edit this template as you like!
"""
import pdb

import bpy
import math

#from ACTR_3D.builer.robots import Mannequin
from ACTR_3D.builder.robots import Manny
from ACTR_3D.builder.robots import Car

from ACTR_3D.builder.sensors import GeometricCamera
#from ACT_v1.builder.actuators import Mannyactuator
#from ACT_v1.builder.sensors.Collision import Collision as LocalCollision
#from ACT_v1.builder.actuators import Torso

from morse.builder import *
#from ACT_v1.builder.actuators import Draw1
#from ACT_v1.builder.sensors import SemanticCamera#Geometriccamerav1
from morse.core.morse_time import TimeStrategies

bpymorse.set_speed(fps=200,logic_step_max=200,physics_step_max=200)

# Add the MORSE mascott, MORSY.
# Out-the-box available robots are listed here:
# http://www.openrobots.org/morse/doc/stable/components_library.html
#
# 'morse add robot <name> ACT_v1' can help you to build custom robots.
#robot = Morsy()
##robot = Human()
##robot.use_world_camera()
##robot.disable_keyboard_control()


#car = Car()
#car.rotate(z=math.radians(0))
#keyboard = Keyboard()
#car.append(keyboard)
#keyboard.properties(ControlType = 'Position')
#going to try manny
robot = Manny()

#car.append(robot)


# The list of the main methods to manipulate your components
# is here: http://www.openrobots.org/morse/doc/stable/user/builder_overview.html
robot.translate(0.0, 0.0, 0.0)


torso = Armature(model_name='ACTR_3D/actuators/Torso.blend', armature_name='Armature')

torso.properties(classpath = "ACTR_3D.actuators.Torso.Torso")
torso.translate(0,0,-0.42)
torso.rotate(z=math.radians(90))


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


robot.append(torso)
torso.add_service('socket')



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
GeometricCamerav1 = GeometricCamera()

GeometricCamerav1.translate(x=0.13,y=-0.0,z=1.22)
GeometricCamerav1.properties(Object=False)
GeometricCamerav1.properties(cam_width=2048,cam_height=2048)
GeometricCamerav1.properties(cam_focal=14)

GeometricCamerav1.rotate(math.radians(180),math.radians(180),math.radians(00))
robot.append(GeometricCamerav1)
#robot.append(GeometricCamerav1)
#geometric1.add_stream('socket')
GeometricCamerav1.add_service('socket')
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
#pose = Pose()
#robot.append(pose)
#pose.translate(z=50)

robot.add_service('socket')


# To ease development and debugging, we add a socket interface to our robot.
#
# Check here: http://www.openrobots.org/morse/doc/stable/user/integration.html 
# the other available interfaces (like ROS, YARP...)
robot.add_default_interface('socket')


# set 'fastmode' to True to switch to wireframe mode
#env = Environment('../projects/ACTR_3D/Left_Hand_Traffic.blend')
env = Environment('../projects/ACTR_3D/target.blend')
#env = Environment('indoors-1/indoor-1')
import math
env.set_camera_location([0, -10, 7])
env.set_camera_rotation([math.radians(80), 0, math.radians(00)])
env.select_display_camera(GeometricCamerav1)
#pdb.set_trace()
#env.set_time_strategy(TimeStrategies.FixedSimulationStepExternalTrigger)
env.configure_stream_manager('socket',time_sync=True,sync_port=5000)
env.show_framerate(True)
#env.show_physics(True)


