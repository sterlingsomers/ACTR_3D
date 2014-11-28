import logging; logger = logging.getLogger("morse.builder." + __name__)
import math
from morse.builder.creator import SensorCreator, bpymorse
from morse.builder.blenderobjects import *
from morse.builder.sensors import *

from morse.core.services import service

class GeometricCamera(VideoCamera):
    _blendname = "camera"
    
    def __init__(self, name=None):
        VideoCamera.__init__(self,name)

        self.properties(Vertical_Flip=False)#cam_width=512,cam_height=512, Vertical_Flip=False)
        self.properties(classpath="ACTR_3D.sensors.GeometricCamera.GeometricCamera")
  

#class GeometricCamera(SemanticCamera):
#    #_classpath = "morse.sensors.semantic_camera.SemanticCamera"
#    _blendname = "camera"
#
#    def __init__(self, name=None):
#        SemanticCamera.__init__(self, name)
#        
#        self.properties(classpath="ACTR_3D.sensors.GeometricCamera.GeometricCamera")
    
 
        