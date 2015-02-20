#import Morse
#from pymorse import Morse

import matplotlib.pyplot as plt
import numpy as np

import ccm
from ccm.pattern import Pattern

import re
#from ccm.pattern import *

#vision_cam = Morse().robot.GeometricCamerav1
import numpy
import math


#vision_cam = ccm.middle.robot.GeometricCamerav1
#from test2 import simu

from ccm.morserobots import middleware

class InternalEnvironment(ccm.Model):
    dial=ccm.Model(isa='dial',value=-1000)
    camp=ccm.Model(isa='dial',value=2000)


class BlenderVision(ccm.Model):
    def __init__(self,buffer1,buffer2,delay=0.0,log=None,delay_sd=None):
        #from ccm.morserobots import middleware
        #self._vision_cam = Morse().robot.GeometricCamerav1
        self._b1=buffer1
        self._b2=buffer2
        self.delay=delay
        self.delay_sd=delay_sd
        self.error=False
        self.busy=False
        self._objects = {}
        self._edges = {}
        self._internalChunks = []

        self._internalChunks.append(ccm.Model(isa='dial'))

        #self._internalEnvironment = InternalEnvironment(self._b1)
        #self._internalEnvironment.doConvert(parent=self)
        #self.blender_camera = Morse().robot.GeometricCamerav1
    
    def getScreenVector(self,x,y):
        x = middleware.request('getScreenVector',[x,y])
        print(x)
        #print(math.sqrt(x[0]**2 + x[1]**2 + x[2]**2))
        #x = numpy.array(middleware.request('getScreenVector',[x,y]))
        #print(numpy.linalg.norm(x))
    
    def cScan(self,openingDepth='0.3'):
        x  = middleware.request('cScan', [openingDepth])
        print(x)

    def xScan(self,openingDepth,y):
        x = middleware.request('xScan', [openingDepth,y])
        print(x)
    
    def almost_equal(self,x1,x2):
        return abs(x1-x2) < 0.01 #1cm?

    def shares_edge(self,list1,list2):
        print(list1, list2)
        if self.almost_equal(list1[0],list2[0]):
            return 1
        if self.almost_equal(list1[0],list2[1]):
            return 1
        if self.almost_equal(list1[1],list2[0]):
            return 1
        if self.almost_equal(list1[1],list2[1]):
            return 1
        return 0


    def find_edges(self):
        for y in sorted(self._objects.keys()):
            if len(list(self._objects[y].keys())) > 1:#there needs to be more than one object to be a depth gap
                edges = []
                edgeCount = 0
                while True:
                    #print(edgeCount,'EDGECOUNT')
                    try:
                        firstLabel,firstvalue = list(self._objects[y].items())[edgeCount]
                    except IndexError:
                        break #or return something

                    for label,value in list(self._objects[y].items())[edgeCount+1:]:
                        if self.shares_edge(firstvalue,value): #if they form an edge
                            edges.append([firstLabel,label])
                    edgeCount+=1
                self._edges[y] = edges
                print(edges,"EDGES")
                #break




    def process_image(self):
        img = middleware.request('get_image',[])



    def scan(self,delay=0.00):
        #print(ccm.middle)
        #import time
        #now = time.time()
        self._objects = middleware.request('scan_image',[])
        ###!!!Note the keys here are strings, not floats
        ###!!Converti them to float below
        self._objects = dict((float(k), v) for k,v in self._objects.items())
        self._ignoreLabels = ['None','Ground']
        #self.find_edges()
        ##print(self._edges)

        #print("Obejects:",self._objects)


        for y in sorted(self._objects.keys()):
            print(y,self._objects[y],"WTF...")

        #Just to plot some stuff
        #######################
        ####PLOTTING###########
        #
        # #Find all labels
        # labels = set()
        # for y in self._objects.keys():
        #     for label in self._objects[y]:
        #         labels.add(label)
        #
        # import pdb
        # #pdb.set_trace()
        # if 'None' in labels:
        #     labels.remove('None')
        # diffs = {}
        # thisValue = 0.0
        # lastValue = 0.0
        # labels = list(labels)
        # for label in labels:
        #     lastValue = -1.0
        #     raws=[]
        #     for y in sorted(self._objects.keys()):
        #         if label in self._objects[y].keys():
        #             thisValue = self._objects[y][label][2]
        #             #if label == 'Ground' and y > 0.2:
        #             #    pdb.set_trace()
        #             #raws.append(thisValue)
        #             if not label in diffs.keys():
        #                 diffs[label] = [[],[]]
        #             if lastValue < 0:
        #                 lastValue = thisValue
        #                 continue
        #             if np.isnan(np.average(np.array(diffs[label][0]))) and lastValue >= 0:
        #                 diffs[label][0].append(abs(thisValue-lastValue))
        #                 diffs[label][1].append(y)
        #                 lastValue = thisValue
        #                 continue
        #             if abs(thisValue-lastValue) <= 2:
        #                 diffs[label][0].append(abs(thisValue-lastValue))
        #                 diffs[label][1].append(y)
        #                 lastValue = thisValue
        # self._ignoreLabels = ['None']#Ignore None from now on
        #
        # for lbl in diffs.keys():
        #     plt.plot(diffs[lbl][1],diffs[lbl][0],label=lbl)
        #     z = np.polyfit(diffs[lbl][1],diffs[lbl][0],3,full=True)
        #     p = np.poly1d(z[0])
        #     xp = np.linspace(min(diffs[lbl][1]),max(diffs[lbl][1]),100)
        #     plt.plot(xp,p(xp),'--')
        #     print(lbl + 'z: ' + repr(z[1]))
        #     if z[1][0] > 0.1:
        #         self._ignoreLabels.append(lbl)
        # plt.show()


                # for ky in self._objects[y]:
                #     #if ky == 'target':
                #         #pdb.set_trace()
                #     if not ky in diffs:
                #         diffs[ky] = [[],[]]
                #     thisValue = self._objects[y][ky][2]
                #     if abs(thisValue-lastValue) < 1:
                #         diffs[ky][0].append(abs(thisValue-lastValue))
                #         diffs[ky][1].append(y)
                #     lastValue = thisValue



        #Collect the ground, near centre
        # diffValues = []
        # Grounds = []
        # ys = []
        # lastValue = 0.0
        # thisValue = 0.0
        # for y in sorted(self._objects.keys()):
        #
        #     try:
        #         thisValue = self._objects[y]['target'][2]
        #     except KeyError:
        #             continue
        #     if not abs(thisValue-lastValue) > 1:
        #         diffValues.append(abs(thisValue-lastValue))
        #         ys.append(y)
        #     lastValue = thisValue
        #
        # diffValues = np.array(diffValues)
        # print("AVERAGE",np.average(diffValues))
        # ys = np.array(ys)
        # z = np.polyfit(ys,diffValues,2,full=True)
        # print("Z", z)
        # p = np.poly1d(z[0])
        # #print(ys)
        # #print(len(y))
        # print(diffValues)
        # xp = np.linspace(min(ys),max(ys),100)
        # plt.plot(ys,diffValues,'-',xp,p(xp),'--')
        # plt.show()

        #Standard Deviations
        # vals = {}
        # for y in sorted(self._objects.keys()):
        #     for ky in self._objects[y]:
        #         if not ky in vals:
        #             vals[ky] = []
        #         vals[ky].append(self._objects[y][ky][3])
        # #print("stds",vals)
        # stds = []
        # plt.plot(vals['RightWall'])
        # plt.show()
        # for key in vals.keys():
        #     print(key)
        #     dVals = np.array(vals[key])
        #     stds.append(np.std(dVals))
        # print("STDS",stds)
        # stds.sort()





        #print(self,._objects.keys(), "HEYSSSSSS")
        #print("Time:")
        #print(time.time() - now)
        #print(self._objects, "objects")
        #yield 1.3

    def refresh(self):
        print ("refresh")
        x = vision_cam.get_visible_objects().result()
        print("refresh2")
        #x = x.result()
        if not x:
            print("No x. ERROR")
            self.error=True
            self.busy=False
            return
        for i in range(len(x)):
            obj_label = x[i]
            if not self._b1.chunk:
                self._b1.set('obj' + repr(i) + ':' + obj_label)
            else:
                #print(dir(self._b1.chunk))
                ck = repr(self._b1.chunk)
                self._b1.set(ck + ' obj' + repr(i) + ':' + obj_label)
        
        #with Morse() as morse:
        #    x = morse.robot.GeometricCamerav1.get_visible_objects()
        #x = vision_cam.get_visible_objects()
        #x = x['visible_objects']
        #for y in x:
        #    print(x, "visible objects")
    
    def check_visibility(self, label):
        return vision_cam.check_visibility(label)
    
    def parse(self,sv_pair):
        '''Given a slot:value pair, returns left and right'''
        return sv_pair.split(':')

    def get_visible_angles(self, label):
        print(vision_cam.get_visible_angles(label))
   
    def request(self,pattern=''):
        print("REQUEST")
        if self.busy: return

        matcher = Pattern(pattern)

        self.error=False
        r=[]
        for obj in self._internalChunks:
            print("one")
            if matcher.match(obj)!=None:
                print("Not None")
        #self._internalEnvironment.__convert()
        #print(dir(self._internalEnvironment), "InternalEnvironment")
        #print(self._internalEnvironment.poop.isa,"poooooooop")
       ## print(matcher.match(self._internalEnvironment), "matcher")

        #print(self.parent, "parent")
        #print(self.parent.parent, "parent.parent")
       # print(self.parent.parent.get_children(), "get_children()")

       # print("CHILDREN")

        #for obj in self.parent.parent.get_children():
        #    print("CHILD",obj)
      ##  if matcher.match(self._internalEnvironment) is not  None:
      ##      print("not none")
        #pattern_list = pattern.split()
        #for p in pattern_list:
        #    (slot,value) = self.parse(p)
        #    if 'obj' in slot:
        #        print('obj')
            
        
#  def request(self,pattern=''):
#    if self.busy: return
#
#    matcher=Pattern(pattern)
#      
#    self.error=False
#    r=[]
#    for obj in self.parent.parent.get_children():
#      if matcher.match(obj)!=None:
#        if not hasattr(obj,'salience') and not hasattr(obj,'visible'):
#          continue
#        
#        if hasattr(obj,'salience'):
#          if self.random.random()>obj.salience:
#            continue
#        if hasattr(obj,'visible'):
#          if obj.visible==False:
#            continue
#        if hasattr(obj,'value'):
#          if obj.value==None:
#            continue
#        r.append(obj)
#
#    self.busy=True
#    d=self.delay
#    if self.delay_sd is not None:
#        d=max(0,self.random.gauss(d,self.delay_sd))
#    yield d
#    self.busy=False
#
#    if len(r)==0:
#      self._buffer.clear()
#      self.error=True
#    else:
#      obj=self.random.choice(r)
#      if obj not in self.parent.parent.get_children():
#        self._buffer.clear()
#        self.error=True
#      elif hasattr(obj,'visible') and obj.visible==False:
#        self._buffer.clear()
#        self.error=True
#      else:
#        self._buffer.set(obj)
      
      
      
        
