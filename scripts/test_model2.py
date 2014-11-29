#Run with a morse environment already running.

#import MiddleMorse
#import Morse
#from pymorse import Morse


#import ACT-R Stuff
import ccm
from ccm.lib.actr import *
#log=ccm.log()
from ccm.morserobots import middleware



  


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

        goal.set('action:meet')

    def meet(goal='action:meet'):
        motor_module.move_forward('0.05')
        motor_module.set_rotation('ribs', '0', '0.5')
        
        goal.set('action:three')

    def three(goal='action:three'):
        motor_module.move_forward('0.05')
        goal.set('action:four')

    def four(goal='action:four'):
        motor_module.move_forward('0.05')
       
        goal.set('action:greet')

    def five(goal='action:five'):
        motor_module.move_forward('0.05')
        goal.set('action:six')

    def six(goal='action:six'):
        motor_module.move_forward('0.05')
        goal.set('stop')

    def stop(goal='stop'):
        self.keepAlive = False
    
        
        

model=MyModel()
ccm.log_everything(model)
model.goal.set('action:greet')

#initialize ACT-R
model.run(0)
model.keepAlive = True
print("Pre-run")

middleware.set_mode('best_effort',2)
#best effort will try to clear the stack
#will tick 10 times for every tick. the defaul py must be set right.

#initial sync
middleware.tick()

while model.keepAlive:

    #model.vision_module.scan()
    model.run(0.01)
    print("TICK...................")
  
    middleware.tick(sync=True)
  

print("post run")
  


