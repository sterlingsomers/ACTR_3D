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
Runs = 20
PopulationSize = 2
sizeSetting = 'small'
sizes = {'large':[48.4,0.7],'small':[42.8,3.5]}
#sizes = {'large':[48.4,0.7],'small':[40.4,2.0]}
#barRatios = [1.0,1.5,2.5]

parameters = {'RadiusMultiplier':[3],
              'VisionMultiplier':[1.135],
              #'ApertureWidth':[48],
              #change for bar
 
              'APRatio':[1.1,1.0,0.9],#0.9,1.0,1.1these are just dummy value for now, indicating 3 apertures to use
              'BarRatio': [2.5,1.5,1.0],#1.0,1.5,2.5],
              'WalkingRate':[0.0128],
              'ProductionSpeed':[0.01],
              'ShoulderRotationRate':[0.020944]}


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
    #for barRatio in barRatios:
        #added apRatio stuff for BAR
    
    wDim = numpy.random.normal(sizes[sizeSetting][0],sizes[sizeSetting][1])
    
    pickle.dump(wDim, open('/sterling/morse/projects/ACTR_3D/params.par','wb'))
        #moved from here...
        #pickle.dump((wDim,apRatio), open('../params.par','wb'))

    for adict in stuffs(parameters):
        #pickle.dump((wDim,adict['BarRatio']), open('/home/sterling/morse/projects/ACTR_3D/params.par','wb'))
        for i in range(Runs):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            timestr = timestr + '.pip'
            path = '/home/sterling/morse/projects/ACTR_3D/scripts/Midrunner_VM135_NoBar/'
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
                #print("ADICTADICTADICTADICT", adict)
                #adict['APRatio']=adict['ApertureWidth']
                
                #adict['ApertureWidth']=adict['APRatio']*wDim*adict['BarRatio']
                #adict['AgentWidth']=wDim/100
                #adict['AgentWithBarWidth']=wDim*adict['BarRatio']/100
                
                #print(wDim,adict['APRatio'],adict['ApertureWidth'],adict['AgentWidth'],adict['AgentWithBarWidth'],adict['BarRatio'])
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



