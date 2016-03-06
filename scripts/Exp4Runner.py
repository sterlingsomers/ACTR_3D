import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking_nonLinear_lessVisualInterference_AFalternate_slower',10,RadiusMultiplier=[1.6,1.7,1.8,1.9,2.0,2.1,2.2],VisionMultiplier=[1.0,1.1],MaximumRotationRate=[0.08])
os.remove('check.ck')

