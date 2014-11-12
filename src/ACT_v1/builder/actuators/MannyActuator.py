from morse.builder.creator import ActuatorCreator

class Mannyactuator(ActuatorCreator):
    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name, \
                                 "ACT_v1.actuators.MannyActuator.Mannyactuator",\
                                 "MannyActuator")

