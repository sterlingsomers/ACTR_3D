#Run with a morse environment already running.


#import Morse
from pymorse import Morse

#import ACT-R Stuff
import ccm
from ccm.lib.actr import *
log=ccm.log()

    
geo = Morse().robot.GeometricCamerav1
motion = Morse().robot.motion
pose = Morse().robot.pose
#semanticL = Morse().cat.semanticL


#To draw stuff on the screen?
draw = Morse().robot.drawer




# define the model
class MyModel(ACTR):
    goal=Buffer()

        
    def greeting(goal='action:greet'):
        #print "Hello"
        goal.set('action:meet')

    def meet(goal='action:meet'):
        data = self.geo.get()
        print(data)
        goal.set('action:three')

    def three(goal='action:three'):
        data = self.geo.get()
        print(data)
        goal.set('action:four')
        
    def four(goal='action:four'):
        goal.set('action:none')
    
    
        
        

model=MyModel()
#x = dir(model)
#print(model,"model1")
model.geo = geo
model.motion = motion
model.pose = pose

ccm.log_everything(model)
#y = dir(model)
#print(len(x),len(y))
#print(set(y)-set(x))
model.goal.set('action:greet')
model.run()
print ("post run")
ccm.finished()


