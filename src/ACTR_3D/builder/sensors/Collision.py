from morse.builder.creator import SensorCreator

class Collision(SensorCreator):
    def __init__(self, name=None):
        SensorCreator.__init__(self, name, \
                               "ACT_v1.sensors.Collision.Collision",\
                               "Collision")

