#from pymorse import Morse


import ccm
#from ccm.pattern import Pattern

import re

from ccm.morserobots import middleware



class BlenderMotorModule(ccm.Model):
    def __init__(self,buffer1,delay=0.0,log=None,delay_sd=None):
        self._b1=buffer1
        #self._b2=buffer2
        self.delay=delay
        self.delay_sd=delay_sd
        self.error=False
        self.busy=False
        #self.blender_camera = Morse().robot.GeometricCamerav1

    def rotate_shoulders_to(self,radians):
        '''Rotates the shoulders by some percentage of maximum rotation.
            Negative rotations are possible.'''
        #print("this is happening....")
        x = torso.set_rotation('ribs',1,radians).result()
            
    def move(self):
        pass

    def lower_arms(self):
        '''Lower the arms'''
        print("Motormodule_sending lower arms")
        middleware.send('lower_arms',[])

    def set_speed(self,speed=0.01):
        '''Move forward @speed in m/s'''
        middleware.send('set_speed',[speed])

    def get_time(self):
        print (middleware.request('get_time',[]))
    
    def async_test2(self,value):
        middleware.send('async_test2',[value])

    def move_forward(self,distance=0.01):
        '''Move forward by some distance'''
        middleware.send('move_forward',[distance])

    def set_rotation(self,bone,axis,radians):
        '''Rotate bone on axis by radians'''
        middleware.send('set_rotation',[repr(bone),axis,radians])
        

