# RadiusMultiplier=[1.9]
# VisionMultiplier=[1.0]
# ApertureWidth=35
# WalkingRate=0.0128
# NT=0
# FName=0
import itertools
import numpy.random
import pickle
import math


Runs = 30
PopulationSize = 5
sizeSetting = 'small'
sizes = {'small':[40.4,2.0]}#{'large':[48.4,0.7]}#,'small':[40.4,2.0]}

parameters = {'RadiusMultiplier':[3.0],
              'VisionMultiplier':[1.135],
              'ApertureWidth':[40,45,50,55,60,65,70],
              'ProductionSpeed':[0.01],
              'WalkingRate':[0.0129],#0.0161],
              'ShoulderRotationRate':[math.radians(120/100)]}

def stuffs(adict):
    keys = list(adict.keys())
    tuples = itertools.product(*[adict[key] for key in keys])
    alist = [{keys[x]:atuple[x] for x in range(len(keys))} for atuple in tuples]
    return alist






import ccm
import os
from subprocess import *
import time
import runpy
import importlib
import multiprocessing as mp

for size in sizes:

    for agent in range(PopulationSize):

        wDim = numpy.random.normal(sizes[size][0],sizes[size][1])
        pickle.dump(wDim, open('../params.par','wb'))

        for adict in stuffs(parameters):
            for i in range(Runs):
                timestr = time.strftime("%Y%m%d-%H%M%S")
                timestr = timestr + '.pip'
                path = '/home/sterling/morse/projects/ACTR_3D/scripts/RotationRate120_VM1139_RM3_small/'
                for file in os.listdir(path):
                    if 'data' in file:
                        os.rename(os.path.join(path,file), os.path.join(path,timestr))


                os.chdir('/home/sterling/morse/projects')
                #subprocess.Popen('morse run ACTR_3D', shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
                #p = subprocess.Popen('ls', shell=True, stdout=subprocess.STDOUT, stderr=subprocess.STDOUT)
                #p.communicate()[0]
                #subprocess.Popen(shlex.split('morse run ACTR_3D'), stdout=subprocess.PIPE,shell=True)
                #call(['morse','run','ACTR_3D'])
                Popen(['gnome-terminal', '--command=morse run ACTR_3D'], stdin=PIPE)
                time.sleep(3)
                os.chdir('/home/sterling/morse/projects/ACTR_3D/scripts')
                try:
                    print("this happens...", i)
                    p = mp.Process(target=runpy.run_module, args=('LinearModel_Planned_LowLevel',adict))
                    p.start()
                    p.join()

                    while p.is_alive():
                        sleep(1)
                    #t = Thread(target=runpy.run_module, args=('LinearModel_Planned_LowLevel'))#(runpy.run_module('LinearModel_Planned_LowLevel',{"RadiusMultiplier":1.9},alter_sys=True)
                    #t.start()

                except RuntimeError:
                    time.sleep(1)
                    continue



