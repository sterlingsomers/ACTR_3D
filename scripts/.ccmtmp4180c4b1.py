
from subprocess import call
import os
import time
import subprocess
from subprocess import *
from sys import executable
import shlex




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




#import ACT-R Stuff
import ccm

#middleware = ccm.morserobots.morse_middleware()
from ccm.lib.actr import *
from ccm.lib.actr.blender_vision import BlenderVision
from ccm.lib.actr.blender_motor_module import BlenderMotorModule


from ccm.morserobots import middleware

class MyEnvironment(ccm.Model):
    v1 = ccm.Model(isa='dial')




class MotorMonitor(ccm.ProductionSystem):

    production_time = 0.05
    fake_buffer = Buffer()

    def init():
        fake_buffer.set('off')#should be 'fake'

    def repeat(fake_buffer='not'):
        #This could be used during movement, actively doing the task
        #bb = middleware.request('getBoundingBox', [])
        motor_module.get_bounding_box()
        motor_module.request_bounding_box()
        motor_module.request('type:proprioception feature:bounding_box width:? depth:?',delay=0.02)

        #print("MONITORING", bb)

class BottomUpVision(ccm.ProductionSystem):
    production_time=0.100
    fake_buffer = Buffer()

    def init():
        fake_buffer.set('fake')

    def repeat(fake_buffer='fake'):
        self.parent.vision_module.scan()


    def detect_obstacles_one(b_vision_command='scan:obstacles get:body_dimensions',motor_module='busy:False'):
        motor_module.request('type:proprioception feature:bounding_box width:? depth:?',delay=0.02)
        b_vision_command.set('scan:obstacles get:visual_obstacles')

    def detect_obstacles_two(b_vision_command='scan:obstacles get:visual_obstacles',
                             b_motor='type:proprioception feature:bounding_box width:?w depth:?d',
                             vision_module='busy:False'):
        vision_module.find_feature(feature='obstacle', depth=d, width=w, delay=0.05)
        vision_module.request('isa:obstacle location:? distance:? angle:?')
        b_vision_command.set('scan:obstacles get:obstacle_found')

    def detect_obstacles_three_fail(b_vision_command='scan:obstacles get:obstacle_found',
                             b_motor='type:proprioception feature:bounding_box width:?w depth:?d',
                             vision_module='error:True'):
        b_vision_command.set('scan:obstacles get:body_dimensions')

    def detect_obstacles_three(b_vision_command='scan:obstacles get:obstacle_found',
                             b_motor='type:proprioception feature:bounding_box width:?w depth:?d',
                             b_vision1='isa:obstacle location:?l distance:? angle:?'):
        self.parent.b_plan_unit.clear()
        b_vision_command.clear()
        goal.set('stop')

class VisionMethods(ccm.ProductionSystem):
    production_time = 0.10
    #fake_buffer = Buffer()
    
    def init():
        pass




class MotorMethods(ccm.ProductionSystem):
    production_time = 0.050
    #fake_buffer = Buffer()



    def slow_step(b_motor_command='walk:true speed:slow'):
        print("producting move_forward")
        motor_module.send('move_forward',amount=0.0645)



class timeKeeper(ccm.Model):



    def record_stop(self,now):
        log.stop = now
        x = 0
        x = middleware.robot_simulation.robot.end_simulation_tasks()
        while not x:
            pass


    def record_start(self,now):

        log.start = now



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
    b_vision_command = Buffer()
    #vm = SOSVision(b_vision)    
    vision_module = BlenderVision(b_vision1,b_vision2,sync=False)
    #p_vision=VisionModule(b_vision1)


    motor_module = BlenderMotorModule(b_motor,sync=False)
    
    bottom_up_vision = BottomUpVision()
    bottom_up_motor = MotorMonitor()

    vm = VisionMethods(b_vision_command)

    b_motor_command = Buffer()
    mm = MotorMethods(b_motor_command)

    
    DMbuffer=Buffer()
    DM=Memory(DMbuffer,latency=0.0)


    b_count=Buffer()

    timeKeep = timeKeeper()

    def init():
        import math
        DM.add('planning_unit:find_target unit_task:find_target')
        DM.add('planning_unit:assess_width unit_task:assess_width')

              
        #DM.add('planning_unit:prepare_for_Take_off unit_task:starter cue:break_on')
        #mm.fake_buffer.set('walk:true speed:slow')
        b_count.set('value:0')
        goal.set('setup:zero')



    ######Calibration########
    def setup_zero_stop(goal='setup:zero',b_count='value:10'):
        b_plan_unit.set('planning_unit:walk_through_aperture')
        b_unit_task.set('unit_task:walk posture:standing')
        b_operator.set('operator:start_walking')
        motor_module.send('rotate_torso',axis=1,radians=math.radians(0))
        motor_module.send('compress_shoulder',bone='shoulder.L',radians=math.radians(0.0))
        motor_module.send('extend_shoulder',bone='shoulder.R',radians=math.radians(0.0))
        goal.clear()
        #goal.set('stop')


    def setup_zero(goal='setup:zero',b_count='value:!10'):
        b_unit_task.set('type:posture standing:true walkable:true minimal_width:true')
        motor_module.send('lower_arms')
        #b_motor_command.set('walk:true speed:slow')
        goal.set('setup:one')

    def setup_one_A(goal='setup:one', b_unit_task='type:posture standing:true walkable:true minimal_width:true'):
        motor_module.send('rotate_torso',axis=1,radians=math.radians(0))
        motor_module.send('compress_shoulder',bone='shoulder.L',radians=math.radians(0.0))
        motor_module.send('extend_shoulder',bone='shoulder.R',radians=math.radians(0.0))
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
        print("Producting get_bounding_box")
        motor_module.get_bounding_box()
        motor_module.request_bounding_box()
        goal.set('setup:four')

    def setup_four(goal='setup:four'):
        motor_module.request('type:proprioception feature:bounding_box width:? depth:?',delay=0.02)
        goal.set('setup:five')

    def setup_five(goal='setup:five',b_motor='width:?w depth:?d'):
        print("setup_five")
        b_cue.set('width:'+w+ ' depth:'+d)
        motor_module.request('type:posture minimal_width:?',delay=0.02)
        goal.set('setup:six')



    def setup_six(goal='setup:six',b_cue='width:?w depth:?d',b_motor='type:posture minimal_width:true standing:?s',
                  b_count='value:?v'):
        print('ADDING:','width:'+w + ' depth:' + d + ' type:posture minimal_width:true' + ' standing:'+s)
        DM.add('width:'+w + ' depth:' + d + ' type:posture minimal_width:true' + ' standing:'+s)
        b_count.modify(value=repr(int(v)+1))
        goal.set('setup:zero')

    def setup_six_failure(goal='setup:six',b_cue='width:?w depth:?d',b_motor='type:posture minimal_width:false standing:?s',
                  b_count='value:?v'):
        print('ADDING:','width:'+w + ' depth:' + d + ' type:posture minimal_width:true' + ' standing:'+s)
        DM.add('width:'+w + ' depth:' + d + ' type:posture minimal_width:true' + ' standing:'+s)
        b_count.modify(value=repr(int(v)+1))
        goal.set('stop')



###########################
###########################
    def start_experiment(b_plan_unit='planning_unit:walk_through_aperture',
                         b_unit_task='unit_task:walk posture:standing',
                         b_operator='operator:start_walking'):

        b_motor_command.set('walk:true speed:slow')
        vision_module.find_feature(feature='opening', depth=0, width=0, delay=0.05)
        vision_module.request('isa:opening centre:? left:? right:?')
        b_operator.set('operator:vision_result')


    def start_experiment_vision_result(b_plan_unit='planning_unit:walk_through_aperture',
                                       b_unit_task='unit_task:walk posture:standing',
                                       b_operator='operator:vision_result',
                                       b_vision1='centre:true'):

        b_vision_command.set('scan:obstacles get:body_dimensions')
        b_operator.clear()


    def start_experiment_vision_no_result(b_plan_unit='planning_unit:walk_through_aperture',
                                          b_unit_task='unit_task:walk posture:standing',
                                          b_operator='operator:vision_result',
                                          vision_module='error:True'):

        b_operator.clear()
        goal.set('stop')

    def start_experiment_vision_not_centre(b_plan_unit='planning_unit:walk_through_aperture',
                                          b_unit_task='unit_task:walk posture:standing',
                                          b_operator='operator:vision_result',
                                          b_vision1='opening:!screenCenter'):

        b_operator.clear()
        goal.set('stop')



    #
    #
    #     b_operator.set('operator:check_for_obstacle')
    #     #b_plan_unit.clear()
    #     #goal.set('stop')
    #     #b_operator.set('operator:visual_monitor_walking')
    #
    #
    # def check_for_obstacle(b_plan_unit='planning_unit:walk_through_aperture',
    #                        b_unit_task='unit_task:walk posture:standing',
    #                        b_operator='operator:check_for_obstacle'):
    #     b_plan_unit.clear()
    #     goal.set('stop')
    #
    # def estimate_passability_retrieveUT(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:none',
    #                                     b_operator='operator:none'):
    #
    #     import math
    #     motor_module.send('rotate_torso',axis=1,radians=math.radians(0))
    #     motor_module.send('compress_shoulder',bone='shoulder.L',radians=math.radians(0.0))
    #     motor_module.send('extend_shoulder',bone='shoulder.R',radians=math.radians(0.0))
    #     #print("fire estimate_passsability_retrieveUT")
    #     DM.request('planning_unit:find_target unit_task:?')
    #     b_operator.set('operator:retrieveUT')
    #     #goal.set('stop')
    #     #b_plan_unit.set('planning_unit:none')
    #
    # def estimate_passability_recalledUT(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:none',
    #                                     b_operator='operator:retrieveUT',
    #                                     DMbuffer='unit_task:?UT'):
    #     #print("fire estimate_passability_recalledUT")
    #     b_unit_task.set('unit_task:' + UT)
    #     b_operator.set('operator:none')
    #     DMbuffer.clear()
    #
    #
    # def estimate_passability_find_opening(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
    #                                         b_operator='operator:none'):
    #
    #     #Make sure bounding box is most up to date
    #     print("producting get_bounding_box (find opening)")
    #     motor_module.get_bounding_box()
    #     motor_module.request_bounding_box()
    #     b_operator.set('operator:get_body_size')
    #
    # def estimate_passability_find_opening_get_body_size(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
    #                                         b_operator='operator:get_body_size'):
    #     #motor_module.get_bounding_box()
    #     motor_module.request('type:proprioception feature:bounding_box width:? depth:?')
    #     b_operator.set('operator:find_opening')
    #
    #
    # def estimate_passability_find_opening_use_body_size(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
    #                                         b_operator='operator:find_opening',b_motor='width:?w depth:?d'):
    #     #motor_module.get_bounding_box()
    #     vision_module.find_feature(feature='opening', depth=d, width=w)
    #     b_plan_unit.set('planning_unit:assess_width')
    #     b_unit_task.set('unit_task:none')
    #     b_operator.set('operator:vision_module_response')
    #     #goal.set('stop')
    #
    #
    #
    # def estimate_passability_found(b_plan_unit='planning_unit:assess_width',
    #                                b_unit_task='unit_task:none',
    #                                b_operator='operator:vision_module_response',
    #                                b_vision1='opening:?opening'):
    #     print("AGENT RESPONSE: YES")
    #     b_plan_unit.clear()
    #     b_unit_task.clear()
    #     b_operator.clear()
    #     goal.set('stop')
    #
    #
    # def estimate_passability_not_found(b_plan_unit='planning_unit:assess_width',
    #                                    b_unit_task='unit_task:none',
    #                                    b_operator='operator:vision_module_response',
    #                                    vision_module='error:True'):
    #     b_plan_unit.set('planning_unit:recall_smallest_width')
    #     b_unit_task.set('unit_task:recall_smallest_width')
    #     b_operator.set('operator:probe_smallest_width')
    #
    # def recall_smallest_width_probe(b_plan_unit='planning_unit:recall_smallest_width',
    #                                 b_unit_task='unit_task:recall_smallest_width',
    #                                 b_operator='operator:probe_smallest_width'):
    #     DM.request('type:posture minimal_width:true standing:true width:? depth:?')
    #     b_operator.set('operator:retrieve_smallest_width')
    #
    #
    # def recall_smallest_width_retrieve(b_plan_unit='planning_unit:recall_smallest_width',
    #                                    b_unit_task='unit_task:recall_smallest_width',
    #                                    b_operator='operator:retrieve_smallest_width',
    #                                    DMbuffer='width:?w depth:?d'):
    #
    #     print("Sucessful Recall.")
    #     b_plan_unit.set('planning_unit:find_target')
    #     b_unit_task.set('unit_task:find_target')
    #     b_operator.set('operator:use_recalled')
    #     b_cue.set('width:' + w + ' depth:' + d)
    #     #goal.set('stop')
    #
    # def recall_smallest_width_retrieval_fail(b_plan_unit='planning_unit:recall_smallest_width',
    #                                          b_unit_task='unit_task:recall_smallest_width',
    #                                          b_operator='operator:retrieve_smallest_width',
    #                                          DM='error:True'):
    #     print("Recall Failed.")
    #     b_plan_unit.clear()
    #     goal.set('stop')
    #
    # def estimate_passability_find_opening_use_recalled(b_plan_unit='planning_unit:find_target', b_unit_task='unit_task:find_target',
    #                                                    b_operator='operator:use_recalled',b_cue='width:?w depth:?d'):
    #     vision_module.find_feature(feature='opening', depth=d, width=w)
    #     b_plan_unit.set('planning_unit:assess_width')
    #     b_unit_task.set('unit_task:none')
    #     b_operator.set('operator:vision_module_response')





    def stop(goal='stop'):
        timeKeep.record_stop(self.now())
        self.keepAlive = False
    
        
        





log=ccm.log(data=True,screen=False,directory="Experiment1_ALLTOPDOWN/default")
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

middleware.set_mode('best_effort',2,sync=False)

#best effort will try to clear the stack
#will tick n times for every tick. the defaul py must be set right.


#initial sync
middleware.tick()

while model.keepAlive:

    #model.vision_module.scan()
    model.run(0.01)
    print("TICK...................")

    middleware.tick()


print("post run")
ccm.finished()
print("here0")
#del ccm
#middleware.robot_simulation.quit()
#middleware.robot_simulation.close()
#middleware.robot_simulation.reset()
#print("here1")

#time.sleep(1)
#print("here2")
#middleware.robot_simulation.close()
#middleware.robot_simulation.close()
middleware.tick()
middleware.robot_simulation.reset()
time.sleep(3)
#middleware.robot_simulation.quit()


#del ccm



