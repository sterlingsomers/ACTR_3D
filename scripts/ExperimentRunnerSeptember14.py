import ccm
import os


ccm.run('LinearModel_Planned_LowLevel',10,RadiusMultiplier=[1.9],VisionMultiplier=[1.0],MaximumRotationRate=[0.08],ApertureWidth=[35,40,45,50,55,60,65,70],WalkingRate=[0.0128,0.0177])
os.remove('check.ck')

