from morse.builder.creator import ActuatorCreator

class Torso(ActuatorCreator):
    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name, \
                                 "ACT-R-Robotics.actuators.Torso.Torso",\
                                 "Torso")

