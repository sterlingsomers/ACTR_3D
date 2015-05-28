import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking',50,RadiusMultiplier=[1.1,1.2])
os.remove('check.ck')

