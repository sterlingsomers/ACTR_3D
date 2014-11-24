from morse.builder.creator import SensorCreator

class Geometriccamerav1(SensorCreator):
    def __init__(self, name=None):
        SensorCreator.__init__(self, name, \
                               "ACT_v1.sensors.GeometricCamerav1.Geometriccamerav1",\
                               "GeometricCamerav1")

