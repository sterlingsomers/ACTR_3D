from morse.builder.creator import ActuatorCreator

class Leftleg(ActuatorCreator):
    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name, \
                                 "ACTR_3D.actuators.LeftLeg.Leftleg",\
                                 "LeftLeg")

