from morse.builder.creator import ActuatorCreator

class Draw1(ActuatorCreator):
    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name, \
                                 "ACT_v1.actuators.Draw1.Draw1",\
                                 "Draw1")

