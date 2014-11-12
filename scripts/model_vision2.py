#Run with a morse environment already running.


#import Morse
from pymorse import Morse

#import ACT-R Stuff
import ccm
from ccm.lib.actr import *
#log=ccm.log()

    
geo = Morse().robot.GeometricCamerav1
torso = Morse().robot.armature


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
    #vision_module = BlenderVision(b_vision1,b_vision2)
    motor_module = BlenderMotorModule(b_motor)
    #Morser=MorseRunner()
        
    def greeting(goal='action:greet'):
        print ("Hello")
        goal.set('action:meet')

    def meet(goal='action:meet'):
        #print(self.geo.use_keys_for_stuff())
        #vision_module.refresh()
        #vision_module.get_visible_angles('RightWall')
        #vision_module.get_visible_angles('LeftWall')
        goal.set('action:three')

    def three(goal='action:three'):
        #vision_module.request('obj0:RightWall distance:?')
        goal.set('action:four')

    def four(goal='action:four'):

        #x = vision_module.scan()
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
        print("action:five...")
        #motor_module.rotate_shoulder(0.1)
        from pymorse import Morse
        x = None
        with Morse() as simu:
            print("doing x...")
            x = simu.robot.GeometricCamerav1.scan_image().result()
        print(x)
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

#x = dir(model)
#print(model,"model1")
model.geo = geo
model.torso = torso
ccm.log_everything(model)
#y = dir(model)
#print(len(x),len(y))
#print(set(y)-set(x))
model.goal.set('action:greet')
model.run(0)
model.keepAlive = True
print("Pre-run")
#while model.keepAlive:
#    model.run(0.01)

with Morse() as simulation:
    
    while model.keepAlive:

        #simulation.tick()
        #print(simulation.time())
        model.run(0.01)
        #simulation.tick()
            
        #print(simulation.time())

	
    
#print("Post run")    
#model.run(2)
#print ("post run")
#ccm.finished()


