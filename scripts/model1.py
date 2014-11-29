#Run with a morse environment already running.

#import MiddleMorse
#import Morse
#from pymorse import Morse


#import ACT-R Stuff
import ccm
from ccm.lib.actr import *
#log=ccm.log()
from ccm.morserobots import middleware



class VisionMethods(ccm.ProductionSystem):
    production_time = 0.01
    fake_buffer = Buffer()
    
    def init():
        fake_buffer.set('fake')

    def repeat(fake_buffer='fake'):
        self.parent.vision_module.scan()    


# define the model
class MyModel(ACTR):
    goal=Buffer()
    
    b_motor = Buffer()#motor buffer. will be VERY complex, likely.
    b_plan_unit=Buffer()
    b_unit_task=Buffer()
    b_cue=Buffer() #allows you to do things systematically, or at least based on previous action - don't end up staring at 1 dial
    b_method=Buffer()
    b_operator=Buffer()
    
    b_vision1 = Buffer()
    b_vision2 = Buffer()
    #vm = SOSVision(b_vision)    
    vision_module = BlenderVision(b_vision1,b_vision2)
    motor_module = BlenderMotorModule(b_motor)
    
    vm = VisionMethods()
    
    DMbuffer=Buffer()
    DM=Memory(DMbuffer,latency=0.0,threshold=None)

    def init():
        DM.add('planning_unit:estimate_passability unit_task:find_opening cue:none')
        
        #DM.add('planning_unit:prepare_for_Take_off unit_task:starter cue:break_on')
        
        b_plan_unit.set('planning_unit:estimate_passability')
        b_unit_task.set('unit_task:get_task')
        b_operator.set('operator:get_task')    


    def estimate_passability_one(b_plan_unit='planning_unit:estimate_passability', b_unit_task='unit_task:get_task'):
        

        goal.set('stop')

    def meet(goal='action:meet'):

        goal.set('action:three')

    def three(goal='action:three'):

        goal.set('action:four')

    def four(goal='action:four'):


      
        goal.set('action:five')

    def five(goal='action:five'):

        goal.set('action:six')

    def six(goal='action:six'):
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
#will tick n times for every tick. the defaul py must be set right.

#initial sync
middleware.tick()

while model.keepAlive:

    #model.vision_module.scan()
    model.run(0.01)
    print("TICK...................")

    middleware.tick(sync=True)

print("post run")
  
   



