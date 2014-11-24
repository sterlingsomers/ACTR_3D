from morse.builder.creator import ActuatorCreator

class Torso(ActuatorCreator):
    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name, \
                                 "ACTR_3D.actuators.Torso.Torso",\
                                 "Torso")
        
        self.properties(classpath="ACTR_3D.actuators.Torso.Torso")
        #self.add_meshes(['Armature'])
