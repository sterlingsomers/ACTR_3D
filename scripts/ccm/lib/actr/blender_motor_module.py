#from pymorse import Morse

from math import pi

import ccm
from ccm.lib.actr import Buffer
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
        self._boundingBox = []
        self.get_bounding_box()

        # self._monitor = MotorMonitor()
                             #internal name  #external       #addition arguments for external
        self.function_map = {'rotate_torso':['set_rotation',{'bone':'ribs'}],
                             'lower_arms':['lower_arms',{}]}

        self._bones = self.get_bones()
        self._boneProperties = {'part.torso':[[0,0],[-pi/4,pi/4],[0,0]]}
        #Tick
        self._internalChunks.append(cmm.Model(type='proprioception',
                                              feature='rotation',
                                              bone='shoulder.R',
                                              rotation0='0.0',
                                              rotation0_quality='min',
                                              rotation1='0.0',
                                              rotation2='0.0',
                                              rotation_quality='min'))

        self._internalChunks.append(cmm.Model(type='proprioception',
                                              feature='rotation',
                                              bone='shoulder.L',
                                              rotation0='0.0',
                                              rotation0_quality='min',
                                              rotation1='0.0',
                                              rotation2='0.0',
                                              rotation_quality='min'))

        self._internalChunks.append(ccm.Model(type='proprioception',
                                              feature='rotation',
                                              bone='torso',
                                              rotation0_quality='none',
                                              rotation0_direction='none',
                                              rotation0='0.0',
                                              rotation1='0.0',
                                              rotation2='0.0'))

        #self._boundingBox = middleware.request('getBoundingBox', [])
        self._internalChunks.append(ccm.Model(type='proprioception',
                                              feature='bounding_box',
                                              width=repr(0.0),
                                              depth=repr(0.0),
                                              height=repr(0.0)))
        #self.blender_camera = Morse().robot.GeometricCamerav1


    def lower_arms(self,function_name,**kwargs):
        pass


    def send(self,function_name,**kwargs):
        '''Checks for function_name in motor module. Calls function_name with kwargs on ACTR side.
            Sends function_name command through middleware to perform function on Morse side.'''
        #ACTR SIDE


        func = getattr(self,function_name)
        func(function_name,**kwargs)

        #Middleware Side
        #Each method should on this side should take care of that
        #So that any restrictions can be handled first
        #kwargs.update(self.function_map[function_name][1])

        #middleware.send(self.function_map[function_name][0],**kwargs)

    def get_bones(self):
        '''This will retrieve all the bones' names'''
        return middleware.request('get_bones',[])


    def rotate_torso(self,function_name,**kwargs):
        '''Rotate ribs on axis by radians'''
        #Check the max rotation
        if self.busy:
            return
        self.busy = True

        maxReached = False
        minReached = False

        kwargs.update(self.function_map[function_name][1])
        print("KW", kwargs)

        minR,maxR = self._boneProperties['part.torso'][kwargs['axis']]
        #print("MINR", minR)
        if kwargs['radians'] > maxR:
            #print("SET TO MAX")
            maxReached=True
            kwargs['radians'] = maxR
        if kwargs['radians'] < minR:
            #print("SET TO MIN")
            minReached = True
            kwargs['radians'] = minR

        #print("RADIANS",radians)
        middleware.send(self.function_map[function_name][0],**kwargs)
        #middleware.send('rotate_torso',axis=axis, radians=radians)
        pattern='type:proprioception bone:torso'
        matcher=Pattern(pattern)
        for obj in self._internalChunks:
            #if axis='0.0'
            if matcher.match(obj)!=None:
                obj.rotation0=kwargs['radians']
                if kwargs['radians'] < 0:
                    object.rotation_direction = 'right'
                if maxReached:
                    obj.rotation0_quality='max'
                if minReached:
                    obj.rotation0_quality='min'
        self.busy=False

    def compress_shoulder(self,function_name,**kwargs):
        pass

    def rotate_shoulders_to(self,radians):
        '''Rotates the shoulders by some percentage of maximum rotation.
            Negative rotations are possible.'''
        #print("this is happening....")
        x = torso.set_rotation('ribs',1,radians).result()

            
    def get_bounding_box(self):
        print("get_bounding_box")
        if self.busy:
            return

        self.busy = True
        self._boundingBox = middleware.request('getBoundingBox', [])
        pattern='type:proprioception feature:bounding_box'
        matcher=Pattern(pattern)
        objs = 0
        for obj in self._internalChunks:
            if matcher.match(obj)!= None:
                objs+=1
                obj.width=repr(self._boundingBox[1])
                obj.depth=repr(self._boundingBox[0])
                obj.height=repr(self._boundingBox[2])
            if objs > 1:
                raise Exception("There shouldn't be more than one match...")
        print("get_bounding_box done.")

        # self._internalChunks.append(ccm.Model(type='proprioception',
        #                                       width=repr(self._boundingBox[0]),
        #                                       depth=repr(self._boundingBox[1]),
        #                                       height=repr(self._boundingBox[2])))
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
            #print("one",obj)
            if matcher.match(obj)!= None:
                r.append(obj)

        self.busy = True
        d = self.delay
        if self.delay_sd is not None:
            d=max(0,self.random.gauss(d,self.delay_sd))
        yield d
        print("YEILDED", d)
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

    # def lower_arms(self):
    #     '''Lower the arms'''
    #     print("Motormodule_sending lower arms")
    #     middleware.send('lower_arms',[])

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
        pass
        #Handle the ACT-R Stuff here
        #  middleware.send('set_rotation',[repr(bone),axis,radians])


