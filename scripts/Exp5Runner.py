import ccm
import os


ccm.run('Experiment0_NoMotorInteferenceWalking_nonLinear_lessVisualInterference_AFalternate_modulated_LINEAR',50,RadiusMultiplier=[1.9],VisionMultiplier=[1.0],MaximumRotationRate=[0.08])
os.remove('check.ck')
