from morse.builder.creator import ActuatorCreator

class Rightleg(ActuatorCreator):
    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name, \
                                 "ACTR_3D.actuators.RightLeg.Rightleg",\
                                 "RightLeg")

