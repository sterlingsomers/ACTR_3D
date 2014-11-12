#Run with a morse environment already running.


#import Morse
from pymorse import Morse

#import ACT-R Stuff
import ccm
from ccm.lib.actr import *
log=ccm.log()

    
geo = Morse().robot.GeometricCamerav1
#semanticL = Morse().cat.semanticL
#semanticR = Morse().cat.semanticR
#semanticM = Morse().mouse.semanticM

#def is_mouse_visible(semantic_camera_stream):
#    data = semantic_camera_stream.get()
#    return data
    

#class MorseRunner(ccm.Model):
#
#    def press(self,letter):
#        l = is_mouse_visible(semanticA1)
#        print(l['visible_objects'])
#        print("yes")




# define the model
class MyModel(ACTR):
    goal=Buffer()
    #Morser=MorseRunner()
        
    def greeting(goal='action:greet'):
        #print "Hello"
        goal.set('action:meet')

    def meet(goal='action:meet'):
        print(self.geo.get())
        goal.set('action:three')

    def three(goal='action:three'):
        
        goal.set('action:none')
    
    
        
        

model=MyModel()
#x = dir(model)
#print(model,"model1")
model.geo = geo
ccm.log_everything(model)
#y = dir(model)
#print(len(x),len(y))
#print(set(y)-set(x))
model.goal.set('action:greet')
model.run()
print ("post run")
ccm.finished()


