from .morseconnection import *



class morse_middleware():
    '''The middleware to handle the connection between ACT-R and Morse.'''
    
    def __init__(self):
        if robot_simulation == None:
            raise Exception("pymorse was not detected, or connection was not successful.")
        
        self.robot_simulation = robot_simulation
        self.mustTick = False
        self.request_dict = {'scan_image':True}
            
        self.action_dict = {'scan_image':['robot_simulation.robot.GeometricCamerav1.scan_image',[]],}
        #{function_name:['absolute path to function', ['args', 'list']]}

        self.cue = []
        

    def request_data(self, datastr):
        '''Passive data, no cue required.'''
        pass

    def request_action(self, datastr, argslist):
        '''Action request. Most actions require a tick. Parallel actions will occur in random order, in following cycles.'''
        if not type(argslist) == list:
            raise Exception("argslist parameter must be a list")
        if datastr in self.request_dict:
            if self.request_dict[datastr]:
                pass
                #That's the indication that it can be run now.
            else:
                pass#can't be run now, something already has, putting in cue. (timing will be off)
        else:
            raise Exception(datastr, "is not in request_dict. It is not available.")

                
                
            
        pass

    def tick(self):
        print("Middleware Tick")
        pass
        

middleware = morse_middleware()               

#connection = robot_simulation

#def tick():
   # print("tick called")
#    connection.tick()



#def _time():
#    return connection.time()
