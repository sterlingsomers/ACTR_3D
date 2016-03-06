import os

path = '/home/sterling/morse/projects/ACTR_3D/scripts/RotationRate120_VM1139_RM3_large'
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
        #now all the variables should be set to the proper values
        afile.close()
        with open("data.csv", "a") as datafile:
            datafile.write(repr(ApertureWidth) + "," +
                           repr(RadiusMultiplier) + "," +
                           repr(VisionMultiplier) + "," +
                           repr(WalkingRate) + "," +
                           repr(angle) + "," + 
                           repr(collision) + "," +
                           repr(direction) + "," +
                           repr(rate) + "," +
                           repr(stop) + "," +
                           repr(time) + "," + 
                           repr(width) + "\n")
        
                
