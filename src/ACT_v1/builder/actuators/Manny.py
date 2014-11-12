from morse.builder.creator import ActuatorCreator

class Manny(ActuatorCreator):
    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name, \
                                 "ACT_v1.actuators.Manny.Manny",\
                                 "Manny")

