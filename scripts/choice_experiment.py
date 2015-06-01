RadiusMultiplier=1.0
VisionMultiplier=1.0
#Run with a morse environment already running.

#import MiddleMorse
#import Morse
#from pymorse import Morse

from subprocess import call
import os
import time
import subprocess
from subprocess import *
from sys import executable
import shlex
import math




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


class CollisionScanner(ccm.ProductionSystem):
    production_time = 0.007
    fake_buffer = Buffer()

    def init():
        fake_buffer.set('none')

    def repeat(fake_buffer='fake'):
        collision = 27
        collision = middleware.robot_simulation.robot.check_collision().result()
        while collision == 27:
            pass

        print("COLLISION", collision)
        #collision = middleware.robot_simulation.robot.collision.get(timeout=0.01)
        #print("Collision", collision)

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
        motor_module.request('type:proprioception feature:bounding_box width:? depth:?',delay=0.01)

        #print("MONITORING", bb)

class VisionScanner(ccm.ProductionSystem):
    production_time=0.080
    fake_buffer = Buffer()

    def init():
        fake_buffer.set('fake')

    def repeat(fake_buffer='fake'):
        self.parent.vision_module.scan()

class BottomUpVision(ccm.ProductionSystem):
    production_time=0.050

    def detect_obstacles_one_alert(b_vision_command='scan:obstacles get:body_dimensions alert_status:alert',motor_module='busy:False'):
        motor_module.request('type:proprioception feature:bounding_box width:? depth:?',delay=0.02)
        b_vision_command.set('scan:obstacles get:visual_obstacles alert_status:alert')

    def detect_obstacles_one(b_vision_command='scan:obstacles get:body_dimensions alert_status:none',motor_module='busy:False'):
        motor_module.request('type:proprioception feature:bounding_box width:? depth:?',delay=0.02)
        b_vision_command.set('scan:obstacles get:visual_obstacles alert_status:none')

    def detect_obstacles_two_alert(b_vision_command='scan:obstacles get:visual_obstacles alert_status:alert',
                             b_motor='type:proprioception feature:bounding_box width:?w depth:?d',
                             vision_module='busy:False'):

        vision_module.find_feature(feature='obstacle', depth=d, width=w, radius_multiplier=self.parent.RadiusMultiplier, delay=0.05)
        vision_module.request('isa:obstacle location:? distance:? radians:?')
        b_vision_command.set('scan:obstacles get:obstacle_found alert_status:alert')

    def detect_obstacles_two(b_vision_command='scan:obstacles get:visual_obstacles alert_status:none',
                             b_motor='type:proprioception feature:bounding_box width:?w depth:?d',
                             vision_module='busy:False'):

        vision_module.find_feature(feature='obstacle', depth=d, width=w, radius_multiplier=self.parent.RadiusMultiplier, delay=0.05)
        vision_module.request('isa:obstacle location:? distance:? radians:?')
        b_vision_command.set('scan:obstacles get:obstacle_found alert_status:none')

    def detect_obstacles_three_fail_alert(b_vision_command='scan:obstacles get:obstacle_found alert_status:alert',
                             b_motor='type:proprioception feature:bounding_box width:?w depth:?d',
                             vision_module='error:True'):
        b_vision_command.set('scan:obstacles get:body_dimensions alert_status:alert')

    def detect_obstacles_three_fail(b_vision_command='scan:obstacles get:obstacle_found alert_status:none',
                             b_motor='type:proprioception feature:bounding_box width:?w depth:?d',
                             vision_module='error:True'):
        b_vision_command.set('scan:obstacles get:body_dimensions alert_status:none')
        #vision_module.error = False

    def detect_obstacles_three_alert(b_vision_command='scan:obstacles get:obstacle_found alert_status:alert',
                             b_motor='type:proprioception feature:bounding_box width:?w depth:?d',
                             b_vision1='isa:obstacle location:?l distance:? radians:?'):
        print("THREE ALERT")
        #sel.parent.b_plan_unit.clear()
        #self.parent.b_operator.set('operator:react isa:obstacle location:' + l)
        #b_vision_command.clear()
        #goal.set('stop')


    def detect_obstacles_three(b_vision_command='scan:obstacles get:obstacle_found alert_status:none',
                             b_motor='type:proprioception feature:bounding_box width:?w depth:?d',
                             b_vision1='isa:obstacle location:?l distance:? radians:?'):
        #self.parent.b_plan_unit.clear()
        self.parent.b_plan_unit.set('planning_unit:walk_through_aperture')
        self.parent.b_unit_task.set('unit_task:walk posture:standing')
        self.parent.b_operator.set('operator:react isa:obstacle location:' + l)
        b_vision_command.clear()
        #goal.set('stop')

class VisionMethods(ccm.ProductionSystem):
    production_time = 0.10
    #fake_buffer = Buffer()
    
    def init():
        pass


class MotorMethods_legs(ccm.ProductionSystem):
    production_time = 0.010

    def slow_step(b_motor_command_legs='walk:true speed:slow', motor_module='busy:False'):
        print("producting move_forward")
        motor_module.send('move_forward',amount=0.00645)
        y_position = middleware.robot_simulation.robot.y_position().result()
        if y_position >= 3.8:
            self.parent.timeKeep.record_data(self.parent.now)

class MotorMethods(ccm.ProductionSystem):
    production_time = 0.010
    #fake_buffer = Buffer()



    def increase_rotation_abdomen_left(b_motor_command_abdomen='rotate:true direction:left', motor_module='busy:False'):
        motor_module.increase_shoulder_rotation('left',0.03491)
        motor_module.increase_shoulder_compression(bone='shoulder.R',radians=0.03491)
        #goal.set('stop')

    def increase_rotation_abdomen_right(b_motor_command_abdomen='rotate:true direction:right', motor_module='busy:False'):
        motor_module.increase_shoulder_rotation('right',-0.03491)
        motor_module.increase_shoulder_compression(bone='shoulder.L',radians=0.03491)
        ##goal.set('stop')

    def increase_rotation_shoulders(b_motor_command_shoulders='rotate:true direction:?d', motor_module='busy:False'):
        pass
        #goal.set('stop')

class timeKeeper(ccm.Model):
    def __init__(self):
        self.start = 0.0
        self.stop = 0.0
        self.recorded = False

    def record_data(self,now):

        if not self.recorded:
            log.angle = math.degrees(self.parent.motor_module.get_shoulder_angle())
            log.direction = self.parent.motor_module.get_shoulder_direction()
        self.recorded = True
        #pythonpylog.delta_time = now - self.start


    def record_stop(self,now):
        self.stop = now
        log.stop = now
        x = 0
        x = middleware.robot_simulation.robot.end_simulation_tasks()
        while not x:
            pass
        log.collision = middleware.robot_simulation.robot.check_collision().result()
        middleware.robot_simulation.robot.reset_collision()
        #log.angle = math.degrees(self.parent.motor_module.get_shoulder_angle())
        #log.direction = self.parent.motor_module.get_shoulder_direction()
        #log.delta_time = self.stop - self.start


    def record_start(self,now):

        self.start = now
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
    collision = CollisionScanner()

    motor_module = BlenderMotorModule(b_motor,sync=False)
    
    bottom_up_vision = BottomUpVision()
    vision_scanner = VisionScanner()
    bottom_up_motor = MotorMonitor()

    vm = VisionMethods(b_vision_command)

    b_motor_command_legs = Buffer()
    b_motor_command_abdomen = Buffer()
    b_motor_command_shoulders = Buffer()

    mm = MotorMethods()
    mm_legs = MotorMethods_legs(b_motor_command_legs)

    
    DMbuffer=Buffer()
    DM=Memory(DMbuffer,latency=0.0)


    b_count=Buffer()

    timeKeep = timeKeeper()

    def init():

        import math
        DM.add('planning_unit:find_target unit_task:find_target')
        DM.add('planning_unit:assess_width unit_task:assess_width')

              

        #mm.fake_buffer.set('walk:true speed:slow')
        b_count.set('value:0')
        #motor_module.send('rotate_torso',axis=1,radians=math.radians(0))
        #motor_module.send('compress_shoulder',bone='shoulder.L',radians=0.0)
        #motor_module.send('compress_shoulder',bone='shoulder.R',radians=0.53)
        #motor_module.increase_shoulder_compression(bone='shoulder.L',radians=0.1)
        #motor_module.increase_shoulder_compression(bone='shoulder.L',radians=0.1)
        #motor_module.increase_shoulder_compression(bone='shoulder.L',radians=0.1)
        #goal.set('stop')
        goal.set('setup:zero')



    ######Calibration########
    def setup_zero_stop(goal='setup:zero',b_count='value:10'):
        #middleware.robot_simulation.robot.check_collision()
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

        #b_motor_command_legs.set('walk:true speed:slow')
        vision_module.find_feature(feature='opening', depth=0, width=0, delay=0.05)
        vision_module.request('isa:opening centre:? left:? right:?')
        timeKeep.record_start(self.now())
        b_operator.clear()
        goal.set('stop')
        #b_operator.set('operator:vision_result')


    def start_experiment_rescan(b_plan_unit='planning_unit:walk_through_aperture',
                                       b_unit_task='unit_task:walk posture:standing',
                                       b_operator='operator:start_rescan'):
        vision_module.find_feature(feature='opening', depth=0, width=0, delay=0.05)
        vision_module.request('isa:opening centre:? left:? right:?')
        b_operator.set('operator:vision_result')


    def start_experiment_vision_result(b_plan_unit='planning_unit:walk_through_aperture',
                                       b_unit_task='unit_task:walk posture:standing',
                                       b_operator='operator:vision_result',
                                       b_vision1='centre:true'):

        b_vision_command.set('scan:obstacles get:body_dimensions alert_status:none')
        b_plan_unit.set('planning_unit:walk_through_aperture')
        b_unit_task.set('unit_task:manage_rotation')
        b_operator.set('operator:retrieve_width')
        #b_vision1.clear()
        #b_operator.set('operator:start_rescan')

    # def start_experiment_vision_no_result2(b_plan_unit='planning_unit:walk_through_aperture',
    #                                       b_unit_task='unit_task:walk posture:standing',
    #                                       b_operator='operator:vision_result',
    #                                       b_vision_command='get:!obstacle_found',
    #                                       vision_module='error:True'):
    #
    #     b_vision_command.clear()
    #     b_operator.clear()
    #     goal.set('stop')


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

    def vision_scan_obstacle_left(b_plan_unit='planning_unit:walk_through_aperture',
                                  b_unit_task='unit_task:walk posture:standing',
                                  b_operator='operator:react isa:obstacle location:left'):
        #Left Shoulder Rotation Start
        #b_operator.set('number:' + repr(3.12))
        b_motor_command_shoulders.set('rotate:true direction:left')
        b_motor_command_abdomen.set('rotate:true direction:left')
        #b_vision_command.set('scan:obstacles get:body_dimensions alert_status:alert')
        #b_plan_unit.clear()
        b_plan_unit.set('planning_unit:walk_through_aperture')
        b_unit_task.set('unit_task:manage_rotation')
        b_operator.set('operator:retrieve_width')
        #goal.set('stop')

    def vision_scan_obstacle_right(b_plan_unit='planning_unit:walk_through_aperture',
                                    b_unit_task='unit_task:walk posture:standing',
                                    b_operator='operator:react isa:obstacle location:right'):
        #Right Shoulder Rotation Start
        #b_operator.set('number:' + repr(3.12))
        b_motor_command_shoulders.set('rotate:true direction:right')
        b_motor_command_abdomen.set('rotate:true direction:right')
        #b_vision_command.set('scan:obstacles get:body_dimensions alert_status:alert')
        #b_plan_unit.clear()
        b_plan_unit.set('planning_unit:walk_through_aperture')
        b_unit_task.set('unit_task:manage_rotation')
        b_operator.set('operator:retrieve_width')
        #goal.set('stop')

    def number_test(b_plan_unit='planning_unit:walk_through_aperture',
                                  b_unit_task='unit_task:walk posture:standing',
                                  b_operator='number:3.12'):
        goal.set('stop')
        b_plan_unit.clear()


    def manage_rotation_check_width(b_plan_unit='planning_unit:walk_through_aperture',
                                    b_unit_task='unit_task:manage_rotation',
                                    b_operator='operator:retrieve_width'):
        motor_module.get_bounding_box()
        motor_module.request_bounding_box()
        motor_module.request('type:proprioception feature:bounding_box width:? depth:?',delay=0.01)
        b_operator.set('operator:check_gap')


    def manage_rotation_check_gap(b_plan_unit='planning_unit:walk_through_aperture',
                                    b_unit_task='unit_task:manage_rotation',
                                    b_operator='operator:check_gap',
                                    b_motor='width:?w depth:?d'):
        print("BBWIDTH",w)
        vision_module.find_feature(feature='opening', width=float(w)*self.VisionMultiplier, depth=d)
        vision_module.request('isa:opening',delay=0.05)
        b_operator.set('operator:check_opening')
        #goal.set('stop')
        #b_plan_unit.clear()

    def manage_rotation_opening_found(b_plan_unit='planning_unit:walk_through_aperture',
                                    b_unit_task='unit_task:manage_rotation',
                                    b_operator='operator:check_opening',
                                    b_vision1='isa:opening'):
        b_motor_command_shoulders.clear()
        b_motor_command_abdomen.clear()
        b_unit_task.set('unit_task:passing_aperture')
        b_operator.set('operator:check_for_aperture')

        #goal.set('stop')
        #b_plan_unit.clear()


    def manage_rotation_opening_not_found(b_plan_unit='planning_unit:walk_through_aperture',
                                    b_unit_task='unit_task:manage_rotation',
                                    b_operator='operator:check_opening',
                                    vision_module='error:True'):
        #b_operator.set('operator:retrieve_width')
        #Have I passed the aperture?
        b_operator.set('operator:check_passed_aperture')
        vision_module.find_feature(feature='opening', width=0, depth=0)
        vision_module.request('isa:opening',delay=0.05)

    def manage_rotation_opening_not_found_still_aperture(b_plan_unit='planning_unit:walk_through_aperture',
                                    b_unit_task='unit_task:manage_rotation',
                                    b_operator='operator:check_passed_aperture',
                                    b_vision1='isa:opening'):
        b_operator.set('operator:retrieve_width')

    def manage_rotation_opening_not_found_no_aperture(b_plan_unit='planning_unit:walk_through_aperture',
                                    b_unit_task='unit_task:manage_rotation',
                                    b_operator='operator:check_passed_aperture',
                                    vision_module='error:True'):
        b_operator.set('operator:double_check_vision')
        vision_module.find_feature(feature='opening', width=0, depth=0)
        vision_module.request('isa:opening',delay=0.05)

    def manage_rotation_opening_not_found_no_aperture_double_check(b_plan_unit='planning_unit:walk_through_aperture',
                                    b_unit_task='unit_task:manage_rotation',
                                    b_operator='operator:double_check_vision',
                                    vision_module='error:True'):
        b_operator.clear()
        goal.set('stop')

    def manage_rotation_opening_not_found_no_aperture_double_check_aperture_visible(b_plan_unit='planning_unit:walk_through_aperture',
                                    b_unit_task='unit_task:manage_rotation',
                                    b_operator='operator:double_check_vision',
                                    b_vision1='isa:opening'):
        b_vision1.clear()
        b_operator.set('operator:check_passed_aperture')

    def passing_aperture_check_for_aperture(b_plan_unit='planning_unit:walk_through_aperture',
                                            b_unit_task='unit_task:passing_aperture',
                                            b_operator='operator:check_for_aperture'):
        vision_module.find_feature(feature='opening',width=0,depth=0)
        vision_module.request('isa:opening',delay=0.05)
        b_operator.set('operator:visual_results')

    def passing_aperture_visual_results(b_plan_unit='planning_unit:walk_through_aperture',
                                        b_unit_task='unit_task:passing_aperture',
                                        b_operator='operator:visual_results',
                                        b_vision1='isa:opening'):
        b_operator.set('operator:check_for_aperture')

    def passing_aperture_visual_results_no_aperture(b_plan_unit='planning_unit:walk_through_aperture',
                                        b_unit_task='unit_task:passing_aperture',
                                        b_operator='operator:visual_results',
                                        vision_module='error:True'):
        b_operator.clear()
        goal.set('stop')








    def stop(goal='stop'):
        timeKeep.record_stop(self.now())
        self.keepAlive = False
    
        
        





log=ccm.log(data=True)
model=MyModel()

model.RadiusMultiplier = RadiusMultiplier
model.VisionMultiplier = VisionMultiplier
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




