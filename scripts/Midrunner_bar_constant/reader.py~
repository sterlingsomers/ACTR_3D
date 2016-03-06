import os
import math

#path = '/home/sterling/Dropbox/SWAT research/Thesis/Data/Nov 1/RotationRate_VisionMultiplier_Search_NOV'
path = os.getcwd()

dictList = []

with open("data.csv", "a") as datafile:
    datafile.write("ApertureWidth," +  
                    "APRatio," + 
                    "AgentWidth," + 
                    "AgentWithBarWidth," + 
                    "BarRatio," +
                    "deltaD," + 
                    "ProductionSpeed," + 
                    "RadiusMultiplier," +
                    "VisionMultiplier," +
                    "WalkingRate," + 
                    "Angle," + 
                    "Collision," + 
                    "Direction," + 
                    "RotationRate," +
                    "StopTime," +
                    "Time," + 
                    "WidthEstimation_FromAgent,\n")


for filename in os.listdir(path):
    
    

    if filename.endswith('.pip'):
        afile = open(os.path.join(path,filename),'r')
        adict = {}
        APRatio = -1
        AgentWidth = -1
        AgentWithBarWidth = -1
        BarRatio = -1
        EstimatedGap = - 1
        ApertureWidth = -1
        RadiusMultiplier = -1
        VisionMultiplier = -1
        WalkingRate = -1
        ProductionSpeed = -1
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
        theta = math.radians(angle)
        try:
            h = AgentWithBarWidth / 2.0
            Dx = ApertureWidth / 2.0 / 100
            a = math.cos(theta) * h
            deltaD = Dx - a
        except TypeError:
            deltaD = None
        
        #now all the variables should be set to the proper values
        afile.close()

 
        
        with open("data.csv", "a") as datafile:
            datafile.write(repr(ApertureWidth / 100) + "," +
                           repr(APRatio) + "," +
                           repr(AgentWidth) + "," + 
                           repr(AgentWithBarWidth) + "," + 
                           repr(BarRatio) + "," + 
                           repr(deltaD) + "," + 
                           repr(ProductionSpeed) + "," + 
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
        
                
