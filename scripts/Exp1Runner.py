import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking_nonLinear_lessVisualInterference',20,RadiusMultiplier=[1.8],VisionMultiplier=[1.0])
os.remove('check.ck')

