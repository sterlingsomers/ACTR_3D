import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking_nonLinear_lessVisualInterference',5,RadiusMultiplier=[1.6,1.7,1.8,1.9,2.0,2.1,2.2],VisionMultiplier=[1.0,1.1])
os.remove('check.ck')

