import logging; logger = logging.getLogger("morse." + __name__)
import morse.core.robot
from morse.helpers.components import add_data, add_property

from morse.core.services import service, async_service, interruptible
from morse.core import status

from morse.core import blenderapi
import bpy
import bge

import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        print("Time out!")
        raise TimeoutException
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class Manny(morse.core.robot.Robot):
    """ 
    Class definition for the Manny robot.
    """

    _name = 'Manny robot'

    def __init__(self, obj, parent=None):
        """ Constructor method

        Receives the reference to the Blender object.
        Optionally it gets the name of the object's parent,
        but that information is not currently used for a robot.
        """
        add_property('_speed', 0.0, 'Speed', 'float',
                    "movement speed of the robot in m/s")

        self._speed = 0.0
        logger.info('%s initialization' % obj.name)
        morse.core.robot.Robot.__init__(self, obj, parent)

        # Do here robot specific initializations
        logger.info('Component initialized')

        #self.module_map = {}
        #self.robot_children = {}#[child for child in self.bge_object.childrenRecursive if 'robot.' in child.name]
        # for child in self._children:
        #     if child.name == 'robot.torso':
        #         self.module_map['robot.torso'] = child
        self.func_map = {}
        self.func_map['move_forward'] = self
        self.func_map['getBones'] = self
        self.func_map['getBoundingBox'] = self



    @service
    def accept_send_request(self,queue):
        print("QUEUE...", queue)
        x = None
        for item in queue:
            meth = getattr(self.func_map[item[0]],item[0])
            x = meth(**item[1])
        return 1
        #import math
        # self.robot_children[0].lower_arms()
        # self.robot_children[0].set_rotation('ribs',1,math.radians(90))
        # self.robot_children[0].set_rotation('ribs',1,math.radians(-25))
        #

        ##print("ASDF",self.components[4].lower_arms())
        # children = [child for child in self.bge_object.childrenRecursive]# if 'part.' in child.name]
        # for child in children:
        #     if child.name == 'part.torso':
        #         print("ACCEPT HERE")
        #         print(child.name)
        #         print(dir(child))


    @service
    def accept_data_request(self,queue):

        print("ACCEPT DATA REQUEST", queue)
        response = {}

        for item in queue:
            print(item[0])
            meth = getattr(self.func_map[item[0]],item[0])
            try:
                with time_limit(2):
                    print("FUNC MAP",self.func_map[item[0]])

                    response[item[0]] = meth(**item[1])
                    print("RESPONSE...",response)
            except TimeoutException:
                print("Timeout in accept_data_request()")
        return response




    def getBones(self):
        children = self.bge_object.childrenRecursive
        children.append(self.bge_object)
        returnList = []
        for child in children:
            if "part" in child.name:
                returnList.append(child.name)
        return returnList


    def getBoundingBox(self):
        try:
            with time_limit(1):

                children = self.bge_object.childrenRecursive
                children.append(self.bge_object)
                #print("self", self.bge_object)
                vxlist = []
                vylist = []
                vzlist = []
                for child in children:#self.bge_object.childrenRecursive:
                    #print(child)
                    if "part" in child.name or child.name == 'robot':
                        #print(child)
                        for mesh in child.meshes:

                            for m_index in range(len(mesh.materials)):
                                for v_index in range(mesh.getVertexArrayLength(m_index)):
                                    vertex = mesh.getVertex(m_index,v_index)
                                    vertex = child.worldTransform * vertex.getXYZ()

                                    vx,vy,vz = vertex[0],vertex[1],vertex[2]
                                    vxlist.append(vx)
                                    vylist.append(vy)
                                    vzlist.append(vz)

                #print(max(vxlist),min(vxlist),max(vylist),min(vylist),max(vzlist),min(vzlist))
                #return self.bge_object.worldOrientation
                return [max(vxlist)-min(vxlist),max(vylist)-min(vylist),max(vzlist)-min(vzlist)]
        except TimeoutException:
            return self.getBoundingBox()


        ####vxlist = []
        ####vylist = []
        ####vzlist = []
        ####for child in self.bge_object.childrenRecursive:

        ####   for mesh in self.bge_object.meshes:
        ####        for m_index in range(len(mesh.materials)):
        ####        for v_index in range(mesh.getVertexArrayLength(m_index)):
        ####            vertex = mesh.getVertex(m_index,v_index)

        ####            print(self.bge_object.worldTransform * vertex.getXYZ()) #worldcoordinates??

        return 1
        ###vxlist = []
        ###vylist = []
        ###vzlist = []
        ###VSLength = self.bge_object.meshes[0].getVertexArrayLength(0)
        ###for vArray in range(0,VSLength):
        ###    vx,vy,vz = self.bge_object.meshes[0].getVertex(0,vArray).getXYZ()
        ###    vxlist.append(vx)
        ###    vylist.append(vy)
        ###    vzlist.append(vz)

        ###print(max(vxlist),min(vxlist),max(vylist),min(vylist),max(vzlist),min(vzlist))

        ###print (dir(self.bge_object.meshes[0]))
        ###print (self.bge_object.childrenRecursive)
        ###for child in self.bge_object.childrenRecursive:
        ###    if 'part' in child.name:
        ###        print (child)
        ###
        ###        VSLength = self.bge_object.meshes[0].getVertexArrayLength(0)
        ###        for vArray in range(0,VSLength):
        ###            vx,vy,vz = child.meshes[0].getVertex(0,vArray).getXYZ()
        ###            vxlist.append(vx)
        ###            vylist.append(vy)
        ###            vzlist.append(vz)
        ###       print(max(vxlist),min(vxlist),max(vylist),min(vylist),max(vzlist),min(vzlist))
        ###
        ###return [max(vxlist)-min(vxlist),max(vylist)-min(vylist),max(vzlist)-min(vzlist)]


        #print(blenderapi.scene().objects, "objects")#bpy.data.objects['Male_Base'].show_bounds()
        #print(dir(blenderapi.objectdata('robot')))
        #blenderapi.objectdata('Male_Base').show_wire=False
        #bpy.data.objects['Male_Base'].show_bounds=True
        #print(self.bge_object.parent)
        #print(dir(self.bge_object.parent))
        #print(bpy.data.objects.keys(),"KEYS")
        #print(bpy.data.objects['Male_Base'].dimensions.y)
        #print(bpy.data.meshes['Male'].materials['skin'].node_tree.nodes.values()[0],"DIR")

        #return 1
        #help(bpy.data.meshes['Male'])
        ##BGE version
        ##vertices = []
        ##vxlist = []
        ##vylist = []
        ##vzlist = []
        ##for child in self.bge_object.childrenRecursive:
        ##    if '_Base' in child.name:
        ##        VSLength = child.meshes[0].getVertexArrayLength(0)
        ##
        ##        for vArray in range(0,VSLength):
        ##            vx,vy,vz = child.meshes[0].getVertex(0,vArray).getXYZ()
        ##            vxlist.append(vx)
        ##            vylist.append(vy)
        ##            vzlist.append(vz)
        ##        #print(min(vxlist),max(vxlist),min(vylist),max(vylist),min(vzlist),max(vzlist))
        ##return [min(vxlist),max(vxlist),min(vylist),max(vylist),min(vzlist),max(vzlist)]

        #    child.visible=not(child.visible)
        #return 1#bpy.data.objects['robot'].bound_box

    @interruptible 
    @async_service
    def set_speed(self, xValue):
        self._speed = xValue
        return 
        
    @service
    def move_forward(self, amount):
        parent = self.bge_object
        parent.applyMovement([amount,0,0],True)
        return amount
        
    def default_action(self):
        """ Main loop of the robot
        """
        vx, vy, vz = 0.0, 0.0, 0.0
        rx, ry, rz = 0.0, 0.0, 0.0

        
        #print(self._speed)        
        vx = self._speed
        
        self.apply_speed('Position', [vx,vy,vz], [rx,ry,rz /2.0])
        self.completed(status.SUCCESS, "Moving Forward")

        #bge.logic.setFrameRate(200)
        #bge.logic.setLogicTicRate(200)
        #bge.logic.setPhysicsTicRate(200)
        # This is usually not used (responsibility of the actuators
        # and sensors). But you can add here robot-level actions.
        #pass
        
