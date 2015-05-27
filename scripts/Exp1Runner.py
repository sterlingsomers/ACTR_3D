import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking',30,RadiusMultiplier=[1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0])
os.remove('check.ck')

