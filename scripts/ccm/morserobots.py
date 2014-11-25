from .morseconnection import *



class morse_middleware():
    '''The middleware to handle the connection between ACT-R and Morse.'''
    
    def __init__(self):
        if robot_simulation == None:
            raise Exception("pymorse was not detected, or connection was not successful.")
        
        self.robot_simulation = robot_simulation
        self.mustTick = False
        self.request_dict = {'scan_image':True,
				'set_speed':True,
                'async_test2':True}
            
        self.action_dict = {'scan_image':['self.robot_simulation.robot.GeometricCamerav1.scan_image',[]],
				'set_speed':['self.robot_simulation.robot.set_speed'],
                'async_test2':['self.robot_simulation.robot.armature.async_test2']}
        #{function_name:['absolute path to function', ['args', 'list']]}
#    def set_speed(self,speed=0.01):
#        '''Move forward @speed in m/s'''
#        x = robo.set_speed(speed).result()
        self.now_queue = []
        self.later_queue = []
        

    def request_data(self, datastr):
        '''Passive data, no cue required.'''
        pass

    def request(self, datastr, argslist):
        '''Action request. Most actions require a tick. Parallel actions will occur in random order, in following cycles.'''
        if not type(argslist) == list:
            raise Exception("argslist parameter must be a list")
        if not all(isinstance(x,str) for x in argslist):
            raise Exception("All arguments have to be strings")
        if datastr in self.request_dict:
            if self.request_dict[datastr]:
                #That's the indication that it can be run now.
                
                rStr = self.action_dict[datastr][0] + '(' + ','.join(argslist) + ')'
                result = eval(rStr)
                return result.result()
                #exec('return self.' + datastr + '(' + ','.join(argslist) + ')')
                #return result
            else:
                pass#can't be run now, something already has, putting in cue. (timing will be off)
        else:
            raise Exception(datastr, "is not in request_dict. It is not available.")

                
                
            
        pass



    def tick(self,sync=False):
        print("Middleware Tick")
        if sync:
            print("sync")
            self.robot_simulation.tick()
        else:
            pass
        

middleware = morse_middleware()
#middleware.tick()               

#connection = robot_simulation

#def tick():
   # print("tick called")
#    connection.tick()



#def _time():
#    return connection.time()
