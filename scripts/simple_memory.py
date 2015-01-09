from ccm.lib.actr import *           # allows use of Python ACT-R
log=ccm.log(everything)
class SimpleModel2(ACTR):            # everything in here defines the model
 
  # first, define the modules within the model  
  goal=Buffer()                 # goal buffer
  retrieval=Buffer()            # a buffer for storing retrieved chunks
  memory=Memory(retrieval)      # the declarative memory system
 
  # now define the productions
  def remember(goal='remember'):   
    memory.request('fact')      # attempt to recall a matching chunk
    goal.set('remembering')
 
  def remembered(goal='remembering',retrieval='fact ?a ?b ?c'):
      print( a,b,c)
      goal.set('done')
 
# now we actually create an instance of the model    
model=SimpleModel2()
 
# add information into declarative memory
model.memory.add('fact cats are cute')
model.memory.add('fact people are strange')
model.memory.add('fact cars go fast')
 
model.goal.set('remember')      # and initialize its goal buffer
model.run() 
