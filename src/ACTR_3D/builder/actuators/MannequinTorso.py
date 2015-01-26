from morse.builder.creator import ActuatorCreator

class MannequinTorso(ActuatorCreator):
    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name, \
                                 "ACTR_3D.actuators.MannequinTorso.Mannequintorso",\
                                 "MannequinTorso")

