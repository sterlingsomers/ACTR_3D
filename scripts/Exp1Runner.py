import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking_nonLinear',5,RadiusMultiplier=[1.6,1.7,1.8,1.9,2.0],VisionMultiplier=[1.0,1.1,1.2])
os.remove('check.ck')

