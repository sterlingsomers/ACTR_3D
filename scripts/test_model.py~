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
        #import math
        motor_module.get_time()
        print ("Hello")
        
        #motor_module.rotate_shoulders_to(math.radians(20))
        
        #motor_module.set_speed(0.002)
        goal.set('action:meet')

    def meet(goal='action:meet'):
        print ("Scan1")
        vision_module.scan()
        print("scan1 complete, set_speed")
        motor_module.set_speed('0.01')
        print("set_speed complete, sync_test2")
        motor_module.async_test2('1')
        #print("time?")
        #motor_module.get_time()
        #print("time complete, scan2")
        vision_module.scan()
        print("scan2 complete")
        #motor_module.get_time()
        #print(self.geo.use_keys_for_stuff())
        #vision_module.refresh()
        #vision_module.get_visible_angles('RightWall')
        #vision_module.get_visible_angles('LeftWall')
        goal.set('action:three')

    def three(goal='action:three'):
        motor_module.get_time()
        #vision_module.request('obj0:RightWall distance:?')
        goal.set('action:four')

    def four(goal='action:four'):
        motor_module.get_time()
        #motor_module.async_test2('2')        
        #motor_module.set_speed('0.01')
        #print('motor set, doing vision')
        #vision_module.scan()
        #print('vision sent')
        #vision_module.scan()


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
        motor_module.get_time()
        #motor_module.rotate_shoulder(0.1)
        #x = vision_module.scan()
        #y = vision_module.scan()
        goal.set('action:six')

    def six(goal='action:six'):
        goal.set('stop')
        #self.torso.shoulder_rotate()
        #print (self.torso.list_IK_targets().result())

    def stop(goal='stop'):
        self.keepAlive = False
    
        
        

model=MyModel()
ccm.log_everything(model)
model.goal.set('action:greet')

#initialize ACT-R
model.run(0)
model.keepAlive = True
print("Pre-run")

middleware.set_mode('best_effort',10)
#best effort will try to clear the stack
#will tick 10 times for every tick. the defaul py must be set right.

#initial sync
middleware.tick()

while model.keepAlive:

        #simulation.tick()
        #print(simulation.time())
    model.run(0.01)
    print("TICK...................")
    #time.sleep(2)
    #pdb.set_trace()
    middleware.tick(sync=True)
    #print ("TIMEajfalfa;", test2.simu.time().result())

    #print (test.x.time())
    #ccm.middleTick()

    #print(ccm.middleTime())
    #morseTick()
        #for i in range(10):
        #    simulation.tick()
            
        #print(simulation.time())

print("post run")
  
   
#model.run(2)
#print ("post run")
#ccm.finished()


