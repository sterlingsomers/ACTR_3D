from morse.builder.creator import ActuatorCreator

class Torso(ActuatorCreator):
    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name, \
                                 "ACT_v1.actuators.torso.Torso",\
                                 "torso")

