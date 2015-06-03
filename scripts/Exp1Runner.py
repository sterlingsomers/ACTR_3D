import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking_nonLinear',50,RadiusMultiplier=[1.4],VisionMultiplier=[1.1])
os.remove('check.ck')

