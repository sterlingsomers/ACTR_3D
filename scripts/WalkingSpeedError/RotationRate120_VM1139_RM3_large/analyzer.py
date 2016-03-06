import os

HumanSmall = []
HumanLarge = []

DataBySize = {} #{Size: [{apertureWidth:x, ...}, {next run},...]

path = '/home/sterling/morse/projects/ACTR_3D/scripts/RotationRate_VisionMultiplier_Search'
dictList = []
for filename in os.listdir(path):

    if filename.endswith('.pip'):
        afile = open(os.path.join(path,filename),'r')
        adict = {}
        ApertureWidth = -1
        RadiusMultiplier = -1
        VisionMultiplier = -1
        WalkingRate = -1
        angle = -1
        collision = -1
        direction = -1
        rate = -1
        stop = -1
        time = -1
        width = -1
        for line in afile:
            if 'direction' in line:
                exec('direction=None')
                continue
            if '=' in line:
                exec(line)
        
        if width in DataBySize:
            DataBySize[width].append{'ApertureWidth':ApertureWidth,
                                    'RadiusMultiplier':RadiusMultiplier,
                                    'VisionMultiplier':VisionMultiplier,
                                    'WalkingRate':WalkingRate,
                                    'angle':angle,
                                    'collision':collision,
                                    'direction':direction,
                                    'rate':rate,
                                    'stop':stop,
                                    'time':time}

        
                
