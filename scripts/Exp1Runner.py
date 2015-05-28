import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking',50,RadiusMultiplier=[1.9])
os.remove('check.ck')

