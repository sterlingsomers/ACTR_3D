import logging; logger = logging.getLogger("morse." + __name__)
from morse.core import blenderapi

import morse.sensors.camera
import morse.sensors.semantic_camera
import morse.helpers.colors

from morse.helpers import passive_objects
from morse.helpers.components import add_data, add_property
from morse.helpers.transformation import Transformation3d

#My additional needs
import numpy
import numpy.linalg

import bpy
import bge
import math

import time

from mathutils import Vector

from morse.core.services import service, async_service
from morse.core import status
#from morse.helpers.components import add_data, add_property

class GeometricCamera(morse.sensors.camera.Camera):
    """Write here the general documentation of your sensor.
    It will appear in the generated online documentation.
    """
    _name = "GeometricCamera"
    _short_desc = "A very basic camera that makes use of blender. Does not do image processing. Intended to send back information to ACTR."

    # define here the data fields exported by your sensor
    # format is: field name, default initial value, type, description
    add_data('distance', 0.0, 'float', 'A dummy odometer, for testing purposes. Distance in meters')
    add_data('color', 'none', 'str', 'A dummy colorimeter, for testing purposes. Default to \'none\'.')
    add_data('visible_objects', [], 'list<objects>',
           "A list containing the different objects visible by the camera. \
            Each object is represented by a dictionary composed of: \n\
                - **name** (String): the name of the object \n\
                - **type** (String): the type of the object \n\
                - **position** (vec3<float>): the position of the \
                  object, in meter, in the blender frame       \n\
                - **orientation** (quaternion): the orientation of the \
                  object, in the blender frame")

    add_property('relative', False, 'relative', 'bool', 'Return object position'
                 ' relatively to the sensor frame.')
    add_property('noocclusion', False, 'noocclusion', 'bool', 'Do not check for'
                 ' objects possibly hiding each others (faster but less '
                 'realistic behaviour)')
    add_property('tag', 'Object',  'tag',  "string",  "The type of "
            "detected objects. This type is looked for as a game property of scene "
            "objects or as their 'Type' property. You must then add fix this "
            "property to the objects you want to be detected by the semantic "
            "camera.")
    def __init__(self, obj, parent=None):
        """ Constructor method.

        Receives the reference to the Blender object.
        The second parameter should be the name of the object's parent.
        """
        logger.info('%s initialization' % obj.name)
        # Call the constructor of the parent class
        morse.sensors.camera.Camera.__init__(self, obj, parent)

        # Locate the Blender camera object associated with this sensor
        main_obj = self.bge_object
        for obj in main_obj.children:
            if hasattr(obj, 'lens'):
                self.blender_cam = obj
                logger.info("Camera object: {0}".format(self.blender_cam))
                break
        if not self.blender_cam:
            logger.error("no camera object associated to the semantic camera. \
                         The semantic camera requires a standard Blender  \
                         camera in its children.")

        # TrackedObject is a dictionary containing the list of tracked objects
        # (->meshes with a class property set up) as keys
        #  and the bounding boxes of these objects as value.
        self.trackedObjects = {}
        for o in blenderapi.scene().objects:
            tagged = ('Type' in o and o['Type'] == self.tag) or (self.tag in o and bool(o[self.tag]))
                               
            if tagged:
                self.trackedObjects[o] = blenderapi.objectdata(o.name).bound_box
                logger.warning('    - %s' % o.name)

        if self.noocclusion:
            logger.info("Semantic camera running in 'no occlusion' mode (fast mode).")
        logger.info("Component initialized, runs at %.2f Hz ", self.frequency)
    
    @service
    def get_visible_objects(self):
        '''Returns the objects visible from this camera'''
        self.local_data['visible_objects'] = []
        visible_object_keys = []
        for obj in blenderapi.persistantstorage().trackedObjects.keys():
            if self._check_visible(obj):
                visible_object_keys.append(passive_objects.label(obj))
                #if 'Wall' in passive_objects.label(obj): #eliminate the other objects for now
                #    visible_object_keys.append(obj)    
        #self.local_data['visible_objects'] = visible_object_keys        
        #return str(visible_object_keys)
        #logger.debug("Visible objects: %s" % self.local_data['visible_objects'])
        return visible_object_keys
            
    
    @service
    def check_visibility(self,label):
        '''Returns True if an object with that label is currently visible'''
        for obj in blenderapi.persistantstorage().trackedObjects.key():
            if self._check_visible(obj):
                if label == passive_objects.label(obj):
                    return 1
        return 0

    @service
    def distance_between_xy(self,x1,y1,x2,y2,minD=0.01,maxD=100,grainSize=0.01):
        distance_to_x1_y1 = self.distance_to_xy(x1,y1,minD,maxD)
        distance_to_x2_y2 = self.distance_to_xy(x2,y2,minD,maxD)
            

    @service
    def distance_to_xy(self,x,y,minD,maxD,grainSize=0.01):
        '''The x,y (screen) should be current.  
        This finds the distance to an object, given x,y coordinate. None if empty space'''
        #print("x",x,"y",y,"minD",minD,"maxD",maxD,"grainSize",grainSize)
        while minD <= maxD:
            hit = self.blender_cam.getScreenRay(x,y,minD)
            if hit:
                return minD
            minD+=grainSize#1cm?
        return maxD

    @service
    def xScan(self,openingDepth,y):
        #import time
        #now = time.time()       
        #return self.blender_cam.lens
        xPartsBig = 250
        maxD = 35.0
        x2s = []
        Edge1 = None
        Edge2 = None
        
        switch = 1
        for x in range(0,50): #250,always test 1, then the neighbour
            #print ("for x", x)
            switch = not switch
            d3d4 = [None,None]
            d1 = self.distance_to_xy(x/50.0,y,0.10,maxD,grainSize=0.15)
            d2 = self.distance_to_xy((x+1)/50.0,y,0.10,maxD,grainSize=0.15)
            #print ("at first if",x,y, x/50.0,(x+1)/50.0, d1, d2, abs(d1-d2))

            if abs(d1-d2) > 1.00: #Just chose a threshold that might work, (1m)... actually does the openingDepth make sense?
                #then it's probably a different object, at a different distance
                #print("at second if", self.blender_cam.getScreenRay(x/50.,y,maxD), self.blender_cam.getScreenRay((x+1)/50.,y,35))
                if self.blender_cam.getScreenRay(x/50.,y,maxD) != self.blender_cam.getScreenRay((x+1)/50.,y,maxD):
                    #Are they different blender objects? Then:
                    #even more likely
                    #fine search starting at x
                    #print("x2 loop")
#WHY DID I * 10? x2*10 or (x2+1) * 10
                    x2 = x - (x/50.0)
                    for bit in range(500):
                        addend = [(x2/50.)+(bit/500.),(x2/50.)+(bit/500.)+(1/500.)]
                        d3d4[0] = self.distance_to_xy(addend[0],y,0.1,maxD,0.01)
                        d3d4[1] = self.distance_to_xy(addend[1],y,0.1,maxD,0.01)
                        #print("X2", (x2/50.)+(bit/500.), (x2/50.)+(bit/500.)+(1/500.),d3d4[0],d3d4[1],abs(d3d4[0]-d3d4[1]))
                        if abs(d3d4[0]-d3d4[1]) > openingDepth:
                            x2s.append([addend[switch],y,d3d4[switch]])
                            #print ("BREAK BREAK BREAK")
                            break
                        
                        #print("in x2 loop")
                        #if (x2*10)/1000. > 1.0:
                        #if (x2*5)/500. > 1.0:    
                        #    break
                        #d3d4[0] = self.distance_to_xy((x2*5)/500.,y,d1-5,maxD,0.01)
                        #d3d4[1] = self.distance_to_xy(((x2*5)+1)/500.,y,d1-5,maxD,0.01)
                        #
                        #print("x2 if", x2,(x2*5)/500.,((x2*5)+1)/500,d3d4[0],d3d4[1],abs(d3d4[0]-d3d4[1]))
                        #if abs(d3d4[0]-d3d4[1]) > openingDepth:
                        #    x2s.append([(x2*5)/500.0,y,d3d4[switch]])
                        #    break
        #print(time.time() - now)
        #print("x2s",x2s)        
        return x2s


    @service
    def ScanBetweenY(self, openingDepth, yRange):
        '''yRange is 2 item list'''
        pass


    @service
    def cScan(self,openingDepth):
        '''Scan's from the centre, organizing based on distances'''
        #hit = self.blender_cam.getScreenRay(0.5,0.5,100)
        #normals = set()
        #for nVerts in range(hit.meshes[0].getVertexArrayLength(0)):
        #    normals.add(repr(hit.meshes[0].getVertex(0,nVerts).normal))
        #    
        #return repr(normals)
        #return self.distance_to_xy(0.5,0.5,0.10,50)
        #using the normals won't work because all cubes are going to have the same set of normals.
        #I will have to assume that different 
        #import time
        #now = time.time()
        #distances = []
        #for i in range(0,500): #250, always test 1, then neighbour
        #    distances.append(self.distance_to_xy(i/500.,0.52,0.05,35.0,grainSize=0.20))#purpose large grainsize 
        #        
        #print('cscan', time.time() - now)
        #
        #return repr(distances)
        import time
        now = time.time()
        spots = []
        for y in range(30):
            #print("y",y/20)
            spots.append(self.xScan(openingDepth,y/30))
        print(time.time() - now)
        return spots
        #for x in spots:
        #    if x:
        #        v1 = numpy.array(self.blender_cam.getScreenVect(x[0][0],x[0][1]))
        #        v2 = numpy.array(self.blender_cam.getScreenVect(x[1][0],x[1][1]))
        #        dot = numpy.dot(v1,v2)
        #        v1_modulus = numpy.sqrt((v1*v1).sum())
        #        v2_modulus = numpy.sqrt((v2*v2).sum())
        #        cos_angle = dot / v1_modulus / v2_modulus
        #        angle = numpy.arccos(cos_angle)
        #        c = x[0][2]
        #        b = x[1][2]
        #        a = numpy.sqrt((-2*b*c*numpy.cos(angle)) + b**2 + c**2)
        #        print(a)
                
                    
                    

    @service
    def getScreenVector(self,x,y):
        normal = numpy.array(self.blender_cam.getScreenVect(0.5,0.5))
        dif = numpy.array(self.blender_cam.getScreenVect(x,y))
        dot = numpy.dot(normal,dif)
        x_modulus = numpy.sqrt((normal*normal).sum())
        y_modulus = numpy.sqrt((dif*dif).sum())
        cos_angle = dot / x_modulus / y_modulus
        angle = numpy.arccos(cos_angle)
        return math.degrees(angle)        
        #cosang = numpy.dot(normal,dif)
        #sinang = numpy.linalg.norm(numpy.cross(normal,dif))
        #return numpy.arctan2(sinang,cosang)
        #return math.degrees(math.acos(numpy.dot(normal,dif)))
            
    @service
    def scan_image(self):
        '''Scans carefully from the Screen. Any object tagged to be skipped, is skipped.
            args:
                    ignoreTage: list of tags to ignore'''
        beginning = time.time()
        objects = {} #{objlable:[inside_angle,outside_angle,highest,lowest]}
        normal = self.blender_cam.getScreenVect(0.5,0.5)
        before = time.time()
        BigGrain = 0.01#1% of the picture
        SmallGrain = 0.0001
        grain = BigGrain
        stepBack = BigGrain
        x = 0.0 #left-> right
        y = 0.0 #top-> bottom
        lastHit = -1
        rowY = 0
        lastY = 0
        lastX = 0
        stateChange = 0.0
        while y < 0.9999:
            #if lastHit != -1:            
                #print(lastHit,objects[lastHit])
            x = 0.0
            lastHit = -1
            while x < 0.9999:
                
                #FDOprint("@x,y", [x,y])
                #if y >= 0.60:
                #    input("continue?")
                stepBack=BigGrain
                hit = self.blender_cam.getScreenRay(x,y,100)#distance of 100#I assume meters.
                #print(ignoreTags)                
                #if repr(hit) == 'None':
                #    x += BigGrain
                #    continue
                #FDOprint("Hit is", hit)
                if lastHit == -1:
                    stepBack=0.0
                if not repr(hit) in objects:#brand new object found (including None(blank space))
                    #FDOprint(hit, "is all new, adding dictionary")
                    objects[repr(hit)] = {}#will contain line by line (y++) the [x1,x2]
                    #print("All new object", hit, objects[hit])
                    #objects[hit].append([x,None,None])
                newState = not(hit == lastHit)
                
                if newState:
                    #FDOprint(hit, "is a new state")
                    if lastHit == -1:#a new line
                        objects[repr(hit)][repr(y)] = [x,None]
                        #FDOprint("added: ", objects[repr(hit)], "because -1")
                        #print("NS", hit, objects[hit])
                    
                    
                    #print("new state", x,y, "from", lastHit, "to", hit)    
                    #if not x:
                    #    x+=grain
                    #    lastHit = hit
                    #    continue
                        
                    stateChange+=1
                    if grain == SmallGrain:
                        #FDOprint("Have a small Grain")
                        #record (x,y)
                        #print("n-", lastHit, objects[lastHit])
                        #FDOprint("X-", lastHit, y,x-grain, hit, y,x)
                        if repr(y) in objects[repr(lastHit)]:#if there is already an entry for this line with that object
                            #FDOprint(y, "in", objects[repr(lastHit)])
                            #FDOprint("so....")
                            objects[repr(lastHit)][repr(y)][1]=x-grain
                            #FDOprint(objects[repr(lastHit)][repr(y)])
                        else:#if this object hasn't been detected on this line
                            #FDOprint(y, "NOT in", objects[repr(lastHit)])
                            #FDOprint("so...")
                            objects[repr(lastHit)][repr(y)]=[x-grain,None]#because it's the most leftest
                            #FDOprint(objects[repr(lastHit)][repr(y)])
                        #objects[hit][y] = [x,None] #roughly... it may already have that entry
                        if repr(y) in objects[repr(hit)]:
                            #FDOprint(y, "in2", objects[repr(hit)])
                            objects[repr(hit)][repr(y)][1]=x #this MIGHT be the end of that object, but it's NOT the beggining, thus [1] in [x,None]
                            #FDOprint("so: ", objects[repr(hit)][repr(y)])
                        else:
                            #FDOprint(y, "NOT in2", objects[repr(hit)])
                            objects[repr(hit)][repr(y)]=[x,None] #if this line is not in there, add it
                            #FDOprint("so: ", objects[repr(hit)][repr(y)])
                                                
                        grain = BigGrain
                        #FDOprint("set to bigGrain")
                        x+=grain
                        lastHit = hit
                        #FDOprint("lasthit = ", hit)
                    else:#grain is big, new state
                        #FDOprint("Big Grain")
                        x-=stepBack
                        #FDOprint("stepback", stepBack)
                        #objects[hit].append([x,None,None])
                        grain=SmallGrain
                        #FDOprint("change to SmallGrain")
                        if not x and not y:
                            grain=BigGrain
                            #FDOprint("change back to BigGrain1")
                        if lastHit == -1:
                            grain=BigGrain
                            #FDOprint("change back to BigGrain2")
                        x+=grain
                        #The lastHit should remain the same because we stepped back but if we do that, it will be -1
                        if grain == SmallGrain:
                            lastHit = lastHit #remains the same because we're moving forward slowly from before the new detection
                            #FDOprint("lastHit = the same", lastHit)
                        else:
                            #FDOprint("lastHit changed to hit->", hit)
                            lastHit = hit#if it's a bigGrain, we're moving forward
                else:
                    #FDOprint("same object found")
                    x+=grain
                    #input("x to " + repr(x) + "continue?")
                    #return "same state" + repr([x,y])
                #if not newState:                
                #    lastHit = hit
            objects[repr(hit)][repr(y)][1]=x#The end (most right) of that line
            #FDOprint("End of the line", objects[repr(hit)][repr(y)], "for", hit, "and", y)
            #FDOlastY = y

            y+=grain
            rowY+=1#a counter for the objects[hit][rowY]
        print(repr(time.time() - beginning) +  " TIME ASDFADFAD")    
        return objects
                               
    @service
    def scan_imageD(self,xyGrain=0.01,xyPrecision=0.0001,depthGrain=0.05,minDepth=0.05,maxDepth=50):
        '''Scans carefully from the Screen. Any object tagged to be skipped, is skipped.
            args:
                    ignoreTage: list of tags to ignore'''
        #depthGrain = depthGrain

        beginning = time.time()
        #objects = {} #{objlable:[inside_angle,outside_angle,highest,lowest]}
        YS = {} #{y-index: {label: [[x1,x2,d1,d2],[..],.],lable2:...}
        normal = self.blender_cam.getScreenVect(0.5,0.5)
        before = time.time()
        BigGrain = 0.01#1% of the picture
        SmallGrain = 0.0001
        grain = BigGrain
        stepBack = BigGrain
        x = 0.0 #left-> right
        y = 0.0 #top-> bottom
        lastHit = -1
        rowY = 0
        lastY = 0
        lastX = 0
        stateChange = 0.0
        while y < 0.9999:
            #if lastHit != -1:
                #print(lastHit,objects[lastHit])
            x = 0.0
            lastHit = -1
            while x < 0.9999:

                #FDOprint("@x,y", [x,y])
                #if y >= 0.60:
                #    input("continue?")
                stepBack=BigGrain
                hit = self.blender_cam.getScreenRay(x,y,100)#distance of 100#I assume meters.
                #print(ignoreTags)
                #if repr(hit) == 'None':
                #    x += BigGrain
                #    continue
                #FDOprint("Hit is", hit)
                if lastHit == -1:
                    stepBack=0.0

                if not y in YS:#change to repr(y) if needed
                    #this is y has just started
                    YS[y] = {}

                newState = not(hit == lastHit)

                if newState:
                    #FDOprint(hit, "is a new state")
                    if lastHit == -1:#a new line
                        #FDOprint('lastHit is -1')
                        YS[y][repr(hit)] = [x,None,self.distance_to_xy(x,y,minDepth,maxDepth,grainSize=depthGrain),None]

                        #FDOprint(YS, "AFTER -1")
                        #objects[repr(hit)][repr(y)] = [x,None]
                        #FDOprint("added: ", objects[repr(hit)], "because -1")
                        #print("NS", hit, objects[hit])


                    #print("new state", x,y, "from", lastHit, "to", hit)
                    #if not x:
                    #    x+=grain
                    #    lastHit = hit
                    #    continue

                    stateChange+=1
                    if grain == SmallGrain:
                        #FDOprint("Have a small Grain")
                        #record (x,y)
                        #print("n-", lastHit, objects[lastHit])
                        #FDOprint("X-", lastHit, y,x-grain, hit, y,x)
                        if repr(lastHit) in YS[y]:#if there is already an entry for this line with that object
                            #FDOprint(y, "in", objects[repr(lastHit)])
                            #FDOprint("so....")
                            YS[y][repr(lastHit)][1]=x-grain
                            YS[y][repr(lastHit)][3]=self.distance_to_xy(x-grain,y,minDepth,maxDepth,grainSize=depthGrain)
                            #FDOprint(objects[repr(lastHit)][repr(y)])
                        else:#if this object hasn't been detected on this line
                            #FDOprint(y, "NOT in", objects[repr(lastHit)])
                            #FDOprint("so...")
                            YS[y][repr(lastHit)]=[x-grain,None,None,None]#because it's the most leftest
                            #FDOprint(objects[repr(lastHit)][repr(y)])
                        #objects[hit][y] = [x,None] #roughly... it may already have that entry
                        if repr(hit)  in YS[y]:
                            #FDOprint(y, "in2", objects[repr(hit)])
                            YS[y][repr(hit)][1]=x #this MIGHT be the end of that object, but it's NOT the beggining, thus [1] in [x,None]
                            YS[y][repr(hit)][3]=self.distance_to_xy(x,y,minDepth,maxDepth,grainSize=depthGrain)
                            #FDOprint("so: ", objects[repr(hit)][repr(y)])
                        else:
                            #FDOprint(y, "NOT in2", objects[repr(hit)])
                            YS[y][repr(hit)]=[x,None,self.distance_to_xy(x,y,minDepth,maxDepth,grainSize=depthGrain),None] #if this line is not in there, add it
                            #FDOprint("so: ", objects[repr(hit)][repr(y)])

                        grain = BigGrain
                        #FDOprint("set to bigGrain")
                        x+=grain
                        lastHit = hit
                        #FDOprint("lasthit = ", hit)
                    else:#grain is big, new state
                        #FDOprint("Big Grain")
                        #FDOprint(YS, 'YS AFTER BIG GRAINss')
                        x-=stepBack
                        #FDOprint("stepback", stepBack)
                        #objects[hit].append([x,None,None])
                        grain=SmallGrain
                        #FDOprint("change to SmallGrain")
                        if not x and not y:
                            grain=BigGrain
                            #FDOprint("change back to BigGrain1")
                        if lastHit == -1:
                            grain=BigGrain
                            #FDOprint("change back to BigGrain2")
                        x+=grain
                        #The lastHit should remain the same because we stepped back but if we do that, it will be -1
                        if grain == SmallGrain:
                            lastHit = lastHit #remains the same because we're moving forward slowly from before the new detection
                            #FDOprint("lastHit = the same", lastHit)
                        else:
                            #FDOprint("lastHit changed to hit->", hit)
                            lastHit = hit#if it's a bigGrain, we're moving forward
                else:
                    #FDOprint("same object found")
                    x+=grain
                    #input("x to " + repr(x) + "continue?")
                    #return "same state" + repr([x,y])
                #if not newState:
                #    lastHit = hit
            #FDOprint (YS, "YS...")
            YS[y][repr(hit)][1]=x#The end (most right) of that line
            YS[y][repr(hit)][3]=self.distance_to_xy(x,y,minDepth,maxDepth,grainSize=depthGrain)
            #FDOprint("End of the line", objects[repr(hit)][repr(y)], "for", hit, "and", y)
            #FDOlastY = y

            y+=grain
            rowY+=1#a counter for the objects[hit][rowY]
        print(repr(time.time() - beginning) +  " TIME ASDFADFAD")
        #print(type(list(YS.keys())[0]))
        return YS

    @service
    def get_visible_angles(self, label):
        '''Returns the screen angles [inside,outside] to the visible
            extent of an object with label'''
        sce = bpy.context.scene        
        obj = sce.objects[label]
        mesh = obj.data
        mat = obj.matrix_world
        vertices =[]
        for vert in mesh.vertices:
            vertices.append(mat*Vector([vert.co[0],vert.co[1],vert.co[2]]))
        #coortinaes of all the vertices
        connections = mesh.edge_keys
        lines = [] #[[nump.array,numpy.array],etc.] two sets of points
        for conn in connections:
            vert1 = vertices[conn[0]]
            vert2 = vertices[conn[1]]
            lines.append([numpy.array(vert1),numpy.array(vert2)])

        #return repr(lines)
        #the indexes of connected vertices
        #convert to numpy?
        vertices = [numpy.array([x.x,x.y,x.z]) for x in vertices if x.z > 0]
        #>0, above the floor.
        
        #which are visible?
        visible_verts = []
        for vert in vertices:
            if self.blender_cam.pointInsideFrustum(vert):
                visible_verts.append(vert)
        return repr(visible_verts)
    
        #return repr(self.blender_cam.getScreenVect(0.5,0.5))
        #return repr(self.blender_cam.getScreenPosition([-3.57,8.9,2.7]))
        return repr(connections)
        #angles = []
        #return angles
    
    def unit_vector(self,vector):
        return vector / numpy.linalg.norm(vector)
    

    def angle_between(self, v1, v2):
        
        #we don't care about z-index
        v1 = v1[0:2]
        v2 = v2[0:2]
        #dx = v1[0] - v2[0]
        #dy = v1[1] - v2[1]
        #deg=0.0    
        #rads = math.atan2(-dy,dx)
        #rads %= 2*math.pi
        #deg = math.degrees(rads)
#       # return deg               
        v1 = self.unit_vector(v1)
        v2 = self.unit_vector(v2)
        angle = numpy.arccos(numpy.clip(numpy.dot(v1,v2),-1,1))
        #angle = numpy.arccos(numpy.dot(v1,v2))
        #if numpy.isnan(angle):
        #    if (v1 == v2).all():
        #        return 0.0
        #    else:
        #        return numpy.pi
        return math.degrees(angle)
    
    @service
    def camera_location(self):
        self.blender_cam.visible = True
        cam_pos =  Vector(self.blender_cam.position)
        #cam_pos = [cam_pos.x,cam_pos.y] #dont' care about z
        #just assume 8.9 for now
        #adjacent = 8.9 - (cam_pos[1])
        hypo2 = Vector([-3.577,8.9,2.7]) - cam_pos
        hypo = self.blender_cam.getVectTo([0.977,8.9,2.7])[1]
        #return repr(cam_pos)
        #return repr(hypo2)
        hypo = numpy.array(hypo)
        orientation = numpy.array([self.blender_cam.orientation[0][0],self.blender_cam.orientation[1][0],self.blender_cam.orientation[2][0]])
        #angle = math.acos(adjacent/hypo)
        #return repr(angle)
        #return repr(cam_pos)
        #return repr(self.blender_cam.worldTransform * Vector(self.blender_cam.position))
        #return repr(self.blender_cam.orientation)
        #if self.blender_cam.pointInsideFrustum([0.97,8.9,2.7]) and self.blender_cam.pointInsideFrustum([-3.57,8.9,2.7]):
        #return repr([self.blender_cam.getVectTo([0.97,8.9,2.7])[0], self.blender_cam.getVectTo([0.97,8.9,2.7])[1], self.blender_cam.getVectTo([-3.57,8.9,2.7])[0], self.blender_cam.getVectTo([-3.57,8.9,2.7])[1]])
        #else:
        #    return 0.0
        
        return repr(self.angle_between(orientation,hypo2))
        return repr(self.blender_cam.orientation)
        return repr(self.blender_cam.getVectTo([0.97,8.9,2.7]))
        ##aVert = [0.97,8.9]
        ##camPos = self.blender_cam.worldTransform * Vector(self.blender_cam.position)
        ##camVert = [camPos.x, camPos.y]
        ##return self.blender_cam.getScreenRay(0.5,0.5)        
        ##return repr(camVert)#repr(self.angle_between(camVert,aVert))


#        aVec = numpy.array(Vector([0.97,8.9,2.7]))
#        camPos = numpy.array(self.blender_cam.worldTransform * Vector(self.blender_cam.position))
#        return repr(self.blender_cam.orientation)
#        return repr(camPos)    
    
    @service
    def get_data_str(self,objStr):
        #blue block
        spot = bge.logic.getCurrentScene().objects['spot']
        #spot.position[0]
        #end blue block
        sce = bpy.context.scene
        obj = sce.objects[objStr]
        mesh = obj.data
        mat = obj.matrix_world
        vertices =[]
        for vert in mesh.vertices:
            vertices.append(mat*Vector([vert.co[0],vert.co[1],vert.co[2]]))
            #this gives me the coordinates of the vectors
        
            #each vertice is a Vector in local. We need to multiply it
            #to get it's global position
        
        connections = mesh.edge_keys
        #for poly in mesh.polygons:
        #    for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
        #        connections.append(mesh.loops[loop_index].vertex_index)
        #connections is now a list of which indexes of vertices are connected


        #find out which lines are visible, up to where
#        if self.blender_cam.boxInsideFrustum(bbox) != self.blender_cam.OUTSIDE:
        #return repr([vertices[connections[0][0]],vertices[connections[0][1]]])
        visible_edges = []
        for conn in connections:
            vert1 = vertices[conn[0]]
            vert2 = vertices[conn[1]]
            #check to increase/decrease x,y, or z of vert1
            startx = 0
            starty = 0
            startz = 0
            endx = 0
            endy = 0
            endz = 0
            x1,y1,z1 = vert1.x, vert1.y, vert1.z
            x2,y2,z2 = vert2.x, vert2.y, vert2.z
            if abs(x1-x2) > 0.1: #accounts for error
                if x1 > x2:
                    startx = x2
                    endx = x1
                elif x2 > x1:
                    startx = x1
                    endx = x2
            elif abs(y1-y2) > 0.1:
                if y1 > y2:
                    starty = y2
                    endy = y1
                elif y2 > x1:
                    starty = y1
                    endy = y2
            elif abs(z1-z2) > 0.1:
                if z1 > z2:
                    startz = z2
                    endz = z1
                elif z2 > z1:
                    startz = z1
                    endz = z2
           #[startx,endx,starty,endy,startz,endz]is the search
            while startx <= endx:
                if self.blender_cam.pointInsideFrustum([startx,y1,z1]):
                    startx = startx + 0.02
                else:
                    break
            spot.position[0] = startx-0.25
            spot.position[1] = y1-0.5
            
            return repr([startx,endx,starty,endy,startz,endz])

                
            #check which of the points are visible
            if self.blender_cam.pointInsideFrustum([vert1.x,vert1.y,vert1.z]):
                visible_edges.append(conn) 
            elif self.blender_cam.pointInsideFrustum([vert2.x,vert2.y,vert2.z]):
                visible_edges.append(conn)           
            #for i in range(len(vert2)):
            #    val1 = vert1[i]
            #    val2 = vert2[i] #assume they're the same is safe.
            #    
            #    if self.blender_cam.pointInsideFrustum(
                #if they're different, we move along that axis
                #from one end to the other
                #need the index
                


        #Both of those together give me the edges of the object
        
        
        #for vert in obj.data.vertices:
        #    vertices.append(vert)
        #return repr([vertices,bge_vertices])
        #return repr(obj.data.edge_keys)
        #obj = bge.logic.getCurrentScene().objects[objStr]
        #if len(obj.meshes) == 1:
        #    mesh = obj.meshes[0]
        #    polyzero = mesh.getPolygon(0)
        #    
        #return help(polyzero.material)
        
    @service
    def use_keys_for_stuff(self):
        
        #render = blenderapi.render.drawLine([1,1,1],[1,5,1],[255,255,255])
        self.local_data['ster']=[]
        visible_object_keys = []
        for obj in blenderapi.persistantstorage().trackedObjects.keys():
            if self._check_visible(obj):
                if 'Wall' in passive_objects.label(obj): #eliminate the other objects for now
                    visible_object_keys.append(obj)
        #self.local_data['ster'].append(len(visible_object_keys))
        
        #The intersectionof "Wall" and all items
        intersection_list = []
        for items in bpy.data.objects:
            #self.local_data['ster'].append(items.name)
            for visible_names in visible_object_keys:
                if visible_names.name in items.name:
                    intersection_list.append(items.name)
        self.local_data['ster'].append(intersection_list)
        #just to see if i can move the square
        sce = bge.logic.getCurrentScene()
        #square = sce.objects['spot']
        for x in sce.objects:
            if 'pot' in x.name:
                #square = x
                x.position[1] = 10
        #help(sce.objects['CameraMesh'])        
        #can i duplicate the square?
        #sce.addObject('spot',square,0)
        #not this way... I can just add a bunch of them.
        
                
        #help(self)
        #for x in sce.objects:
        #    if x.name == 'Cube':
        #        help(x)
                
        #me = bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False,
        #location=(0.0,0.1,6.0),rotation=(0,0,0))
        #me = bpy.ops.mesh.primitive_cube_add(location=(0,0,5))
        #x = repr(dir(me))
        #ob = bpy.data.objects.new('Cube01',me)
        #sce = bge.logic.getCurrentScene()
        #sce.addObject(me)
        
        #help(me)
        #scene = bpy.context.scene
        #objects = list(scene.objects)
        #me.update()
        #scene.update()
        vertices_RW = []
        RW = sce.objects['RightWall']
        RWscale = 1
        #wTransform = RW.worldTransform
        #RWdata = bpy.data.meshes.keys()#['RightWall']
        
        for mesh in RW.meshes:
            for m_index in range(len(mesh.materials)):
                for v_index in range(mesh.getVertexArrayLength(m_index)):
                    vertex = mesh.getVertex(m_index, v_index)
                    vertices_RW.append(vertex)
        LW = sce.objects['LeftWall']
        vertices_LW = []
        for mesh in LW.meshes:
            for m_index in range(len(mesh.materials)):
                for v_index in range(mesh.getVertexArrayLength(m_index)):
                    vertex = mesh.getVertex(m_index, v_index)
                    vertices_LW.append(vertex)
                    
        globalLWs = []
        for item in vertices_LW:
            
            x = item.x
            y = item.y
            z = item.z
            P = Vector([x,y,z])
            globalLWs.append(LW.worldTransform * P)
            #M = LW.worldOrientation
            
            #globalLWs.append(LW.worldPosition + M * P)
            
            
        #dDistance = self.distance_between(RW,LW)
        return (intersection_list,len(bpy.data.objects),repr(sce.objects['CameraMesh'].worldPosition))
        
            #for visible_names in visible_object_keys:
                #if visible_names in items:
                 #   intersection_list.append(items)
        #self.local_data['ster'].append(repr(intersection_list))                   
#        self.local_data['ster'].append(repr(list(bpy.data.objects)))
        
        #bpy.ops.mesh.primitive_uv_sphere_add(segments=12, size=3,enter_editmode=False,location=(1,1,1))
        

    
    
    @service
    def distance_between(self, objLabel1, objLabel2):
        '''Returns the distance between object (by label). iff the objects are visible'''
        if objLabel1 in self.get_visible_objects() and objLabel2 in self.get_visible_objects():
            obj1 = bge.logic.getCurrentScene().objects[objLabel1]
            obj2 = bge.logic.getCurrentScene().objects[objLabel2]
            if obj1 and obj2:
                return self.distance_between_objects(obj1,obj2)
        else:
            return -1
        
    def distance_between_objects(self, object1, object2):
        #Should be able to list comprehension this...
        distances = []
        object1_vertices = []
        for mesh in object1.meshes:
            for m_index in range(len(mesh.materials)):
                for v_index in range(mesh.getVertexArrayLength(m_index)):
                    vertex = mesh.getVertex(m_index, v_index)
                    x = vertex.x
                    y = vertex.y
                    z = vertex.z
                    P = Vector([x,y,z])
                    P = object1.worldTransform * P
                    object1_vertices.append(numpy.array(P))
                            
        object2_vertices = []
        for mesh in object2.meshes:
            for m_index in range(len(mesh.materials)):
                for v_index in range(mesh.getVertexArrayLength(m_index)):
                    vertex = mesh.getVertex(m_index, v_index)
                    x = vertex.x
                    y = vertex.y
                    z = vertex.z
                    P = Vector([x,y,z])
                    P = object2.worldTransform * P 
                    object2_vertices.append(numpy.array(P))
                    
        for items1 in object1_vertices:
            for items2 in object2_vertices:
                distances.append(numpy.linalg.norm(items1-items2))
        #return nArrays2
        distances = [math.fabs(x) for x in distances]    
        return min(distances)
        
    def _inspect_mesh(self,obj):
        
        #obj.applyRotation([00.1,0,0])
        #print( obj.meshes[0].numPolygons, "num")
        #print(obj.meshes[0].getPolygon(0), "polygon")
       # print(obj.worldScale,"scale")
        #p1 = obj.meshes[0].getPolygon(0)
        #print(p1.getMaterialIndex(),"index")
        #thismat = obj.meshes[0].materials[0]
        #print(obj.meshes[0].materials[0], "materials")
        #v0 = obj.meshes[0].getVertex(0,0)
        #v0.color=[0.0, 0.0, 0.0, 0.0]
        #print(obj.meshes[0].getVertex(0,0), "vertex")
        #print(dir(obj.meshes[0].getPolygon(0)))
        return repr(obj.meshes[0].numPolygons) + 'poly'
        
    @service
    def get_current_distance(self):
        """ This is a sample (blocking) service (use 'async_service' decorator
        for non-blocking ones).

        Simply returns the value of the internal counter.

        You can access it as a RPC service from clients.
        """
        logger.info("%s is %sm away" % (self.name, self.local_data['distance']))

        return self.local_data['distance']

#    def default_action(self):
#        """ Main loop of the sensor.
#
#        Implements the component behaviour
#        """#
#
#        import random
#
#        # implement here the behaviour of your sensor
#
#        self.local_data['distance'] = self.position_3d.x # distance along X in world coordinates
#
#        # our test sensor sees a random color
#        self.local_data['color'] = random.choice(["blue", "red", "green", "yellow"])
#
