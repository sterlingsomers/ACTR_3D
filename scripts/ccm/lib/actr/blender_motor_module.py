#from pymorse import Morse


import ccm
from ccm.pattern import Pattern

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
        self._internalChunks = []
        self._boundingBox = None
        self.get_bounding_box()
        #self.blender_camera = Morse().robot.GeometricCamerav1

    def rotate_torso(self,axis,radians):
        '''Rotate ribs on axis by radians'''
        middleware.send('set_rotation_ribs',[repr('ribs'),axis,radians])


    def rotate_shoulders_to(self,radians):
        '''Rotates the shoulders by some percentage of maximum rotation.
            Negative rotations are possible.'''
        #print("this is happening....")
        x = torso.set_rotation('ribs',1,radians).result()
            
    def get_bounding_box(self):
        self._boundingBox = middleware.request('getBoundingBox', [])
        self._internalChunks.append(ccm.Model(type='proprioception',
                                              width=repr(self._boundingBox[0]),
                                              depth=repr(self._boundingBox[1]),
                                              height=repr(self._boundingBox[2])))
        # self._internalChunks.append(ccm.Model(isa='dial'))

    def move(self):
        pass

    def request(self,pattern=''):
        print("REQUEST")
        if self.busy: return

        matcher = Pattern(pattern)
        print("Matcher",matcher)

        self.error=False
        r=[]
        for obj in self._internalChunks:
            print("one")
            if matcher.match(obj)!= None:
                r.append(obj)

        self.busy = True
        d = self.delay
        if self.delay_sd is not None:
            d=max(0,self.random.gauss(d,self.delay_sd))
        yield d
        self.busy=False
        if len(r) == 0:
            self._b1.clear()
            self.error = True
        else:
            obj=self.random.choice(r)
            self._b1.set(obj)
    # if self.busy: return
    #
    # matcher=Pattern(pattern)
    #
    # self.error=False
    # r=[]
    # for obj in self.parent.parent.get_children():
    #   if matcher.match(obj)!=None:
    #     print("Not None")
    #     if not hasattr(obj,'salience') and not hasattr(obj,'visible'):
    #       continue
    #
    #     if hasattr(obj,'salience'):
    #       if self.random.random()>obj.salience:
    #         continue
    #     if hasattr(obj,'visible'):
    #       if obj.visible==False:
    #         continue
    #     if hasattr(obj,'value'):
    #       if obj.value==None:
    #         continue
    #     r.append(obj)
    #
    # self.busy=True
    # d=self.delay
    # if self.delay_sd is not None:
    #     d=max(0,self.random.gauss(d,self.delay_sd))
    # yield d
    # self.busy=False
    #
    # if len(r)==0:
    #   self._buffer.clear()
    #   self.error=True
    # else:
    #   obj=self.random.choice(r)
    #   if obj not in self.parent.parent.get_children():
    #     self._buffer.clear()
    #     self.error=True
    #   elif hasattr(obj,'visible') and obj.visible==False:
    #     self._buffer.clear()
    #     self.error=True
    #   else:
    #     self._buffer.set(obj)

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
        

