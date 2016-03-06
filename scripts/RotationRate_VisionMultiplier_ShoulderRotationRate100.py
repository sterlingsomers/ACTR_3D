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
Runs = 10
PopulationSize = 3
sizeSetting = 'large'
sizes = {'large':[48.4,0.7],'small':[40.4,2.0]}

parameters = {'RadiusMultiplier':[2.5,3.0],
              'VisionMultiplier':[1.135,1.137,1.139],
              'ApertureWidth':[40,55],
              'WalkingRate':[0.0128],
              'ShoulderRotationRate':[math.radians(100/100)]}

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


for agent in range(PopulationSize):

    wDim = numpy.random.normal(sizes[sizeSetting][0],sizes[sizeSetting][1])
    pickle.dump(wDim, open('../params.par','wb'))

    for adict in stuffs(parameters):
        for i in range(Runs):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            timestr = timestr + '.pip'
            path = '/home/sterling/morse/projects/ACTR_3D/scripts/RotationRate_VisionMultiplier_ShoulderRotationRate100/'
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



