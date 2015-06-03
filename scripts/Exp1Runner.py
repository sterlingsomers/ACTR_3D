import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking_nonLinear',20,RadiusMultiplier=[1.5,1.6,1.7],VisionMultiplier=[1.0,1.1])
os.remove('check.ck')

