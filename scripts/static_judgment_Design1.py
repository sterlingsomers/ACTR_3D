#Run with a morse environment already running.

#import MiddleMorse
#import Morse
#from pymorse import Morse


#import ACT-R Stuff
import ccm

#middleware = ccm.morserobots.morse_middleware()
from ccm.lib.actr import *
from ccm.lib.actr.blender_vision import BlenderVision
from ccm.lib.actr.blender_motor_module import BlenderMotorModule
#log=ccm.log()
from ccm.morserobots import middleware

class MyEnvironment(ccm.Model):
    v1 = ccm.Model(isa='dial')

#class VisionModule(ccm.Model):
#    poop=ccm.Model(isa='dial',value=-1000)


class MotorMonitor(ccm.ProductionSystem):

    production_time = 0.01
    fake_buffer = Buffer()

    def init():
        fake_buffer.set('fake')#should be 'fake'

    def repeat(fake_buffer='fake'):
        #This could be used during movement, actively doing the task

        print("MONITORING")

class VisionMethods(ccm.ProductionSystem):
    production_time = 0.030
    fake_buffer = Buffer()
    
    def init():
        fake_buffer.set('fake')#should be 'fake'

    def repeat(fake_buffer='notnot'):
        #This could be used during movement, actively doing the task

        self.parent.vision_module.scan()
        #self.parent.vision_module.getScreenVector('0.4999','0.5')    
        #self.parent.vision_module.cScan('0.5')#50cm minimum depth for an opening.
        #self.parent.vision_module.xScan('0.3','0.5')
        




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
    #p_vision=VisionModule(b_vision1)


    motor_module = BlenderMotorModule(b_motor)
    
    vm = VisionMethods()
    mm = MotorMonitor()
    
    DMbuffer=Buffer()
    DM=Memory(DMbuffer,latency=0.0)




    def init():
        DM.add('planning_unit:find_target unit_task:find_target')
        DM.add('planning_unit:assess_width unit_task:assess_width')
              
        #DM.add('planning_unit:prepare_for_Take_off unit_task:starter cue:break_on')
        

        goal.set('setup:zero')


    ######Calibration########
    def setup_zero(goal='setup:zero'):
        motor_module.lower_arms()
        goal.set('setup:one')

    def setup_one(goal='setup:one'):
        import math
        motor_module.rotate_torso('1',repr(math.radians(-90.0)))
        goal.set('setup:two')

    def setup_two(goal='setup:two'):
        motor_module.get_bounding_box()
        goal.set('setup:three')
        #goal.set('stop')


    def setup_three(goal='setup:three'):
        motor_module.request('type:proprioception feature:bounding_box width:?')
        goal.set('setup:four')

    def setup_four(goal='setup:four',b_motor='width:?w height:?h depth:?d'):

        b_cue.set('width:' + w + ' height:' + h + ' depth:'+d)
        motor_module.request('type:proprioception feature:rotation bone:torso rotation0:?')
        goal.set('setup:five')

    def setup_five(goal='setup:five',b_motor='feature:rotation bone:torso rotation0:?rZero rotation1:?rOne rotation2:?rTwo'):
        b_cue.chunk['rotation0'] = rZero
        b_cue.chunk['bone'] = 'torso'
        b_cue.chunk['feature'] = 'rotation'
        #b_cue.set(b_cue.chunk + 'rotation0:' + rZero)
        print(b_cue.chunk)
        DM.add(b_cue.chunk)
        goal.set('setup:six')

# '''Notes:
#     We can see already a problem with this approach.
#     The amount of information to be stored in DM would be very high
#         including multiple bones and their rotation
#         and then some way of storing whether it is a min or max width.
#         It makes this approach very difficult to support.
#     The logic would be:
#     a) is there an opning of sufficient depth
#         b) what is the width of that opening?
#     c) without >,< operators, cannot check whether there is a stored DM with that depth
#     b-alternate) given a pre-stored minimum width, is the opening bigger.
#         In that case, the < > operators are in the module.'''

    def setup_six(goal='setup:six'):
        #import math
        #motor_module.rotate_torso('1',repr(math.radians(0.0)))
        #motor_module.get_bounding_box()
        goal.set('stop')



        #motor_module.request('type:proprioception width:?')
        #goal.set('stop')






        #b_plan_unit.set('planning_unit:find_target')
        #b_unit_task.set('unit_task:none')
        #b_operator.set('operator:none')
        #b_cue.set('cue:none')


        #import math
        #input new model stuffs here:
        #self.motor_module.rotate_torso('0',repr(math.radians(90)))

        #self.motor_module.lower_arms()
        #self.motor_module.set_speed('0.01')

        #import math

        #self.motor_module.set_rotation('ribs','0',repr(math.radians(90)))
        #self.motor_module.set_rotation('arm_upper.R','0',repr(math.radians(35)))

        #get bounding box here.
        #self.cd momiddleware.request('getBoundingBox', [])

    def estimate_passability_retrieveUT(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:none',
                                        b_operator='operator:none'):
        print("fire estimate_passsability_retrieveUT")
        DM.request('planning_unit:find_target unit_task:?')
        b_operator.set('operator:retrieveUT')
        #vision_module.find_opening()
        #motor_module.request('width:?')
        #self.middleware.request('getBoundingBox', [])
        #b_cue.set('cue:retrieving_task')
        #goal.set('stop')
        #b_plan_unit.set('planning_unit:none')

    def estimate_passability_recalledUT(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:none',
                                        b_operator='operator:retrieveUT',
                                        DMbuffer='unit_task:?UT'):
        b_unit_task.set('unit_task:' + UT)
        b_operator.set('operator:none')
        DMbuffer.clear()

    def estimate_passability_find_opening(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
                                            b_operator='operator:none'):
        #vision_module.cScan()
        #print("estimate_passability_find_opening")
        #vision_module.request('isa:dial')
        #goal.set('stop')
        motor_module.lower_arms()
        b_operator.set('operator:get_body_size')

    def estimate_passability_find_opening_get_body_size(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
                                            b_operator='operator:get_body_size'):
        #motor_module.get_bounding_box()
        motor_module.request('width:?')
        b_operator.set('operator:find_opening')

    def estimate_passability_find_opening_use_body_size(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
                                            b_operator='operator:find_opening',b_motor='width:?x'):
        #motor_module.get_bounding_box()
        vision_module.find_feature(feature='opening', depth=x)
        b_plan_unit.set('planning_unit:assess_width')
        b_unit_task.set('unit_task:none')
        b_operator.set('operator:none')



    def estimate_passability_assess_width_noUT(b_plan_unit='planning_unit:assess_width',
                                            b_unit_task='unit_task:none',
                                            b_operator='operator:none'):
        DM.request('planning_unit:assess_width unit_task:?')
        import math
        motor_module.rotate_torso('1',repr(math.radians(00.0)))
        b_operator.set('operator:retrieveUT')
        
    def estimate_passability_assess_width_recall_UT(b_plan_unit='planning_unit:assess_width',
                                            b_unit_task='unit_task:none',
                                            b_operator='operator:retrieveUT'):
        #DM.request('planning_unit:assess_width unit_task:?')
        #b_oprator.set('operator:retrieveUT')

        motor_module.get_bounding_box()
        motor_module.request('width:?')
        goal.set('stop')
    #def estimate_passability_two(b_plan_unit='planning_unit:estimate_passability',
    #                             b_unit_task='unit_task:get_task',
    #                             b_cue='cue:retrieving_task', DMbuffer='unit_task:?UT'):
    #    
    #    print(UT)
    #    goal.set('stop')




    def stop(goal='stop'):
        self.keepAlive = False
    
        
        

model=MyModel()
model.middleware = middleware
#vInternal = VisualEnvironment()
env = MyEnvironment()
env.agent = model

ccm.log_everything(env)
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
  
   



