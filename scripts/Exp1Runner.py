import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking',20,RadiusMultiplier=[1.0],VisionMultiplier=[1.0,1.1,1.2,1.3])
os.remove('check.ck')

