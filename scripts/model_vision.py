#Run with a morse environment already running.

#import MiddleMorse
#import Morse
#from pymorse import Morse


#import ACT-R Stuff
import ccm
from ccm.lib.actr import *
#log=ccm.log()
import ccm.morserobots as morserobots



    


class Tools(ccm.Model):
    def process_matrix_string(self,matrixStr):
        print(matrixStr.split())

# define the model
class MyModel(ACTR):
    goal=Buffer()
    
    b_motor = Buffer()

    
    b_vision1 = Buffer()
    b_vision2 = Buffer()
    #vm = SOSVision(b_vision)    
    vision_module = BlenderVision(b_vision1,b_vision2)
    motor_module = BlenderMotorModule(b_motor)
    #Morser=MorseRunner()
        
    def greeting(goal='action:greet'):
        import math
        
        print ("Hello")
        
        motor_module.rotate_shoulders_to(math.radians(20))
        
        motor_module.set_speed(0.002)
        goal.set('action:meet')

    def meet(goal='action:meet'):
        #print(self.geo.use_keys_for_stuff())
        vision_module.refresh()
        #vision_module.get_visible_angles('RightWall')
        #vision_module.get_visible_angles('LeftWall')
        goal.set('action:three')

    def three(goal='action:three'):
        vision_module.request('obj0:RightWall distance:?')
        goal.set('action:four')

    def four(goal='action:four'):

        x = vision_module.scan()
        y = vision_module.scan()
        #print(x)
        #print(self.geo.scan_image())
        #print(self.geo.get_some_data())
        #print(self.geo.get_data_str('RightWall'))
        #print(self.geo.camera_location())
        #tools.process_matrix_string(matrixStr)
        #exec('mtx = ' + matrixStr)
        #print(mtx)        
        goal.set('action:five')

    def five(goal='action:five'):
        #motor_module.rotate_shoulder(0.1)
        x = vision_module.scan()
        #y = vision_module.scan()
        goal.set('action:six')

    def six(goal='action:six'):
        goal.set('stop')
        #self.torso.shoulder_rotate()
        #print (self.torso.list_IK_targets().result())

    def stop(goal='stop'):
        self.keepAlive = False
    
        
        

model=MyModel()
#model.r=test2.simu.robot
#x = dir(model)
#print(model,"model1")
#model.geo = geo
#model.torso = torso
ccm.log_everything(model)
#y = dir(model)
#print(len(x),len(y))
#print(set(y)-set(x))
model.goal.set('action:greet')
model.run(0)
#ccm.middleTick()
model.keepAlive = True
print("Pre-run")
#while model.keepAlive:
#    model.run(0.01)

#with Morse() as simulation:
#print(ccm.middle)
import time
morserobots.tick()
print(morserobots.time(),"TIME1")
morserobots.tick()
while model.keepAlive:

        #simulation.tick()
        #print(simulation.time())
    model.run(0.01)
    print("TICK...................")
    #time.sleep(2)
    #pdb.set_trace()
    morserobots.tick()
    #print ("TIMEajfalfa;", test2.simu.time().result())

    #print (test.x.time())
    #ccm.middleTick()

    #print(ccm.middleTime())
    #morseTick()
        #for i in range(10):
        #    simulation.tick()
            
        #print(simulation.time())

	
    
print("Post run")
print(morserobots.time(),'TIME2')
morserobots.tick()    
#model.run(2)
#print ("post run")
#ccm.finished()


