RadiusMultiplier=1.9
VisionMultiplier=1.0
ApertureWidth=35
WalkingRate=0.0177
NT=1
FName='LinearModel_Planned_LowLeve'
import ccm
ccm.log(data=True,screen=False,directory="Midrunner/RadiusMultiplier(1.9) WalkingRate(0.0177) NT(1) FName(LinearModel_Planned_LowLeve)")
print("AP", ApertureWidth)
print("NT", NT)

import ccm
import os
from subprocess import *
import time
import importlib


for i in range(NT):
    if not os.path.isfile('check.ck'):
        os.chdir('/home/sterling/morse/projects')
        #subprocess.Popen('morse run ACTR_3D', shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        #p = subprocess.Popen('ls', shell=True, stdout=subprocess.STDOUT, stderr=subprocess.STDOUT)
        #p.communicate()[0]
        #subprocess.Popen(shlex.split('morse run ACTR_3D'), stdout=subprocess.PIPE,shell=True)
        #call(['morse','run','ACTR_3D'])
        Popen(['gnome-terminal', '--command=morse run ACTR_3D'], stdin=PIPE)
        time.sleep(3)
        os.chdir('/home/sterling/morse/projects/ACTR_3D/scripts')
        f = open('check.ck', 'w')
        f.close()

    ccm.run("LinearModel_Planned_LowLevel",1)
    time.sleep(2)
    print("this happens....................................")
    #del ccm
    importlib.reload(ccm)
    os.remove('check.ck')



