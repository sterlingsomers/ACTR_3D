#Run with a morse environment already running.

#import MiddleMorse
#import Morse
#from pymorse import Morse

from subprocess import call
import os
import time
import subprocess
import shlex
os.chdir('/home/sterling/morse/projects')
subprocess.Popen(shlex.split('morse run ACTR_3D'), stdout=subprocess.PIPE)
#call(['morse','run','ACTR_3D'])
time.sleep(3)
os.chdir('/home/sterling/morse/projects/ACTR_3D/scripts')
#import ACT-R Stuff
import ccm

#middleware = ccm.morserobots.morse_middleware()
from ccm.lib.actr import *
from ccm.lib.actr.blender_vision import BlenderVision
from ccm.lib.actr.blender_motor_module import BlenderMotorModule

from ccm.morserobots import middleware

class MyEnvironment(ccm.Model):
    v1 = ccm.Model(isa='dial')

#class VisionModule(ccm.Model):
#    poop=ccm.Model(isa='dial',value=-1000)


class MotorMonitor(ccm.ProductionSystem):

    production_time = 0.01
    fake_buffer = Buffer()

    def init():
        fake_buffer.set('asdf')#should be 'fake'

    def repeat(fake_buffer='fake'):
        #This could be used during movement, actively doing the task
        #bb = middleware.request('getBoundingBox', [])
        print("MONITORING", bb)

class VisionMethods(ccm.ProductionSystem):
    production_time = 0.10
    fake_buffer = Buffer()
    
    def init():
        fake_buffer.set('nonono')#should be 'fake'

    def repeat(fake_buffer='fake'):
        #This could be used during movement, actively doing the task

        self.parent.vision_module.scan()
        #self.parent.vision_module.getScreenVector('0.4999','0.5')    
        #self.parent.vision_module.cScan('0.5')#50cm minimum depth for an opening.
        #self.parent.vision_module.xScan('0.3','0.5')


class MotorMethods(ccm.ProductionSystem):
    production_time = 0.050
    fake_buffer = Buffer()

    def slow_step(fake_buffer='walk:true speed:slow'):
        motor_module.send('move_forward',amount=0.0645)






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
    mm = MotorMethods()

    
    DMbuffer=Buffer()
    DM=Memory(DMbuffer,latency=0.0)


    b_count=Buffer()

    def init():
        DM.add('planning_unit:find_target unit_task:find_target')
        DM.add('planning_unit:assess_width unit_task:assess_width')
              
        #DM.add('planning_unit:prepare_for_Take_off unit_task:starter cue:break_on')
        #mm.fake_buffer.set('walk:true speed:slow')
        b_count.set('value:0')
        goal.set('setup:zero')



    ######Calibration########
    def setup_zero_stop(goal='setup:zero',b_count='value:10'):
        #goal.set('stop')

        b_plan_unit.set('planning_unit:find_target')
        b_unit_task.set('unit_task:none')
        b_operator.set('operator:none')
        goal.clear()

    def setup_zero(goal='setup:zero',b_count='value:!10'):
        b_unit_task.set('type:posture standing:true walkable:true minimal_width:true')
        motor_module.send('lower_arms')
        goal.set('setup:one')

    def setup_one_A(goal='setup:one', b_unit_task='type:posture standing:true walkable:true minimal_width:true'):
        goal.set('setup:two')
        b_operator.set('direction:left')

    def setup_one_B(goal='setup:one', b_unit_task='type:posture standing:true walkable:true minimal_width:true'):
        goal.set('setup:two')
        b_operator.set('direction:right')

    def setup_two_left(goal='setup:two',b_unit_task='type:posture standing:true walkable:true minimal_width:true',
                       b_operator='direction:left'):
        import math
        motor_module.send('rotate_torso',axis=1,radians=math.radians(90))
        motor_module.send('extend_shoulder',bone='shoulder.L',radians=math.radians(50.0))
        motor_module.send('compress_shoulder',bone='shoulder.R',radians=math.radians(50.0))
        #motor_module.send('move_forward',amount=0.01)
        goal.set('setup:three')
        #goal.set('stop')

    def setup_two_right(goal='setup:two',b_unit_task='type:posture standing:true walkable:true minimal_width:true',
                        b_operator='direction:right'):
        import math
        motor_module.send('rotate_torso',axis=1,radians=math.radians(-90))
        motor_module.send('compress_shoulder',bone='shoulder.L',radians=math.radians(50.0))
        motor_module.send('extend_shoulder',bone='shoulder.R',radians=math.radians(50.0))
        #motor_module.send('move_forward',amount=0.01)

        goal.set('setup:three')
        #goal.set('stop')

    def setup_three(goal='setup:three'):
        motor_module.get_bounding_box()
        goal.set('setup:four')

    def setup_four(goal='setup:four'):
        motor_module.request('type:proprioception feature:bounding_box width:? depth:?')
        goal.set('setup:five')

    def setup_five(goal='setup:five',b_motor='width:?w depth:?d'):
        b_cue.set('width:'+w+ ' depth:'+d)
        motor_module.request('type:posture minimal_width:?')
        goal.set('setup:six')

    def setup_six(goal='setup:six',b_cue='width:?w depth:?d',b_motor='type:posture minimal_width:?m standing:?s',
                  b_count='value:?v'):
        print('ADDING:','width:'+w + ' depth:' + d + ' type:posture minimal_width:' + m + ' standing:'+s)
        DM.add('width:'+w + ' depth:' + d + ' type:posture minimal_width:' + m + ' standing:'+s)
        b_count.modify(value=repr(int(v)+1))
        goal.set('setup:zero')



###########################
###########################



    def estimate_passability_retrieveUT(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:none',
                                        b_operator='operator:none'):

        import math
        motor_module.send('rotate_torso',axis=1,radians=math.radians(0))
        motor_module.send('compress_shoulder',bone='shoulder.L',radians=math.radians(0.0))
        motor_module.send('extend_shoulder',bone='shoulder.R',radians=math.radians(0.0))
        #print("fire estimate_passsability_retrieveUT")
        DM.request('planning_unit:find_target unit_task:?')
        b_operator.set('operator:retrieveUT')
        #goal.set('stop')
        #b_plan_unit.set('planning_unit:none')

    def estimate_passability_recalledUT(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:none',
                                        b_operator='operator:retrieveUT',
                                        DMbuffer='unit_task:?UT'):
        #print("fire estimate_passability_recalledUT")
        b_unit_task.set('unit_task:' + UT)
        b_operator.set('operator:none')
        DMbuffer.clear()


    def estimate_passability_find_opening(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
                                            b_operator='operator:none'):

        #Make sure bounding box is most up to date
        motor_module.get_bounding_box()
        b_operator.set('operator:get_body_size')

    def estimate_passability_find_opening_get_body_size(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
                                            b_operator='operator:get_body_size'):
        #motor_module.get_bounding_box()
        motor_module.request('type:proprioception feature:bounding_box width:? depth:?')
        b_operator.set('operator:find_opening')


    def estimate_passability_find_opening_use_body_size(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
                                            b_operator='operator:find_opening',b_motor='width:?w depth:?d'):
        #motor_module.get_bounding_box()
        vision_module.find_feature(feature='opening', depth=d, width=w)
        b_plan_unit.set('planning_unit:assess_width')
        b_unit_task.set('unit_task:none')
        b_operator.set('operator:vision_module_response')
        #goal.set('stop')



    def estimate_passability_found(b_plan_unit='planning_unit:assess_width',
                                   b_unit_task='unit_task:none',
                                   b_operator='operator:vision_module_response',
                                   b_vision1='opening:?opening'):
        print("AGENT RESPONSE: YES")
        b_plan_unit.clear()
        b_unit_task.clear()
        b_operator.clear()
        goal.set('stop')


    def estimate_passability_not_found(b_plan_unit='planning_unit:assess_width',
                                       b_unit_task='unit_task:none',
                                       b_operator='operator:vision_module_response',
                                       vision_module='error:True'):
        b_plan_unit.set('planning_unit:recall_smallest_width')
        b_unit_task.set('unit_task:recall_smallest_width')
        b_operator.set('operator:probe_smallest_width')

    def recall_smallest_width_probe(b_plan_unit='planning_unit:recall_smallest_width',
                                    b_unit_task='unit_task:recall_smallest_width',
                                    b_operator='operator:probe_smallest_width'):
        DM.request('type:posture minimal_width:true standing:true width:? depth:?')
        b_operator.set('operator:retrieve_smallest_width')


    def recall_smallest_width_retrieve(b_plan_unit='planning_unit:recall_smallest_width',
                                       b_unit_task='unit_task:recall_smallest_width',
                                       b_operator='operator:retrieve_smallest_width',
                                       DMbuffer='width:?w depth:?d'):

        print("Sucessful Recall.")
        b_plan_unit.set('planning_unit:find_target')
        b_unit_task.set('unit_task:find_target')
        b_operator.set('operator:use_recalled')
        b_cue.set('width:' + w + ' depth:' + d)
        #goal.set('stop')

    def recall_smallest_width_retrieval_fail(b_plan_unit='planning_unit:recall_smallest_width',
                                             b_unit_task='unit_task:recall_smallest_width',
                                             b_operator='operator:retrieve_smallest_width',
                                             DM='error:True'):
        print("Recall Failed.")
        b_plan_unit.clear()
        goal.set('stop')

    def estimate_passability_find_opening_use_recalled(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
                                                       b_operator='operator:use_recalled',b_cue='width:?w depth:?d'):
        vision_module.find_feature(feature='opening', depth=d, width=w)
        b_plan_unit.set('planning_unit:assess_width')
        b_unit_task.set('unit_task:none')
        b_operator.set('operator:vision_module_response')





    def stop(goal='stop'):
        self.keepAlive = False
    
        
        





log=ccm.log(html=True)
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
ccm.finished()
print("here0")
del ccm
#middleware.robot_simulation.quit()
#middleware.robot_simulation.close()
#middleware.robot_simulation.reset()
#print("here1")

#time.sleep(1)
#print("here2")
#middleware.robot_simulation.close()
#middleware.robot_simulation.close()
middleware.tick(sync=True)
middleware.robot_simulation.quit()




