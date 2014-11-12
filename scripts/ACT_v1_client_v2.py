#! /usr/bin/env python3
"""
Test client for the <ACT_v1> simulation environment.

This simple program shows how to control a robot from Python.

For real applications, you may want to rely on a full middleware,
like ROS (www.ros.org).
"""


import sys

try:
    from pymorse import Morse
except ImportError:
    print("you need first to install pymorse, the Python bindings for MORSE!")
    sys.exit(1)

print("Use WASD to control the robot")

with Morse() as simu:
    
    motion = simu.robot.motion
    pose = simu.robot.pose
    geo = simu.robot.GeometricCamerav1
    armature = simu.robot.armature
    #collision = armature.armcollision
    #proximity = simu.robot.armature.armproximity

    
    #draw = geo.drawFlag
        
       
    v = 0.0
    w = 0.0
    
    left = 0.0
    
    while True:
        key = input("WASD-rt-c-n?")
        
        if key.lower() == "w":
            v += 0.1
        elif key.lower() == "s":
            v -= 0.1
        elif key.lower() == "a":
            w += 0.1
        elif key.lower() == "d":
            w -= 0.1
        elif key.lower() == "r":
            armature.set_rotation(0.2)
        elif key.lower() == "t":
            armature.set_rotation(-0.2)
        
        
        #elif key.lower() == "n":
        #    #print("Nothing...")
        #    #data = proximity.get()
        #    #print(data)
        #    data = collision.get(timeout=0.1)
        #    print(repr(data) + "asdf")
                    
        elif key.lower() == "c":
            data=geo.get()
            print(data)
        elif key.lower() == "b":
            print( geo, pose)#geo.level('draw')
            

        
            
        else:
            continue

      # here, we call 'get' on the pose sensor: this is a blocking
      # call. Check pymorse documentation for alternatives, including
      # asynchronous stream subscription.
        print("The robot is currently at: %s" % pose.get())

        motion.publish({"v": v, "w": w})
        #torso.publish({"left": left})
