from .morseconnection import *



class morse_middleware():
    '''The middleware to handle the connection between ACT-R and Morse.'''
    
    def __init__(self):
        if robot_simulation == None:
            raise Exception("pymorse was not detected, or connection was not successful.")
        
        self.robot_simulation = robot_simulation
        self.mustTick = False
        self.modes = ['best_effort']
        self.send_dict = {'set_speed':True,
                        'async_test2':True} #{function_name:blocking?}

        self.request_dict = {'scan_image':False,
                'get_time':True}
            
        self.action_dict = {'scan_image':['self.robot_simulation.robot.GeometricCamerav1.scan_image',[]],
				'set_speed':['self.robot_simulation.robot.set_speed'],
                'async_test2':['self.robot_simulation.robot.armature.async_test2'],
                'get_time':['self.robot_simulation.time']}

        self.danger_list = ['get_time']
        #{function_name:['absolute path to function', ['args', 'list']]}
#    def set_speed(self,speed=0.01):
#        '''Move forward @speed in m/s'''
#        x = robo.set_speed(speed).result()
        self.send_queue = [] #contains [[datastr,argslist],[datastr,argslist]]
        

    def send(self, datastr, argslist):
        '''send a command, no response required. If a blocking command, pushed to next tick cycle.'''
        if not type(argslist) == list:
            raise Exception("argslist parameter must be a list")
        if not all(isinstance(x,str) for x in argslist):
            raise Exception("All arguments have to be strings")
        if datastr in self.send_dict:
            if not self.mustTick:
            #Can run it now, but must block future
                if self.send_dict[datastr]:
                    #It is non-blocking
                    rStr = self.action_dict[datastr][0] + '(' + ','.join(argslist) + ')'
                    eval(rStr)
                else:
                    #it is blocking
                    self.mustTick = True
                    rStr = self.action_dict[datastr][0] + '(' + ','.join(argslist) + ')'
                    eval(rStr)
                    #no return, it's a command being sent. Assume it worked.
            else:
                if self.mode == 'best_effort':
                    self.send_queue.append([datastr,argslist])
                else:
                    raise Exception(datastr + " dropped. Use best_effort mode to use multiple blocking sends.")


        else:
            raise Exception(datastr + " is not in send_dict. It is not available.")
                    
        
            
        
        

    def request(self, datastr, argslist):
        '''Request data. Most actions require a tick. Parallel actions will occur in random order, in following cycles.'''
        if not type(argslist) == list:
            raise Exception("argslist parameter must be a list")
        if not all(isinstance(x,str) for x in argslist):
            raise Exception("All arguments have to be strings")
        #if self.mustTick:#blocking command send/request has been made already
        #    raise Exception("A blocking even has already occured.")

        if datastr in self.request_dict:
            if self.request_dict[datastr]:#is it blocking?
                if self.mustTick:#already blocking?
                    raise Exception("A blocking event has already occured")
                self.mustTick = True
                rStr = self.action_dict[datastr][0] + '(' + ','.join(argslist) + ')'
                result = eval(rStr)
                if 'return' in dir(result):
                    result = result.result()
                return result #must be returned right away because it's a request
            else:
                #no mustTick, it's not blocking
                rStr = self.action_dict[datastr][0] + '(' + ','.join(argslist) + ')'
                result = eval(rStr)
                if 'return' in dir(result):
                    result = result.result()
                return result
                
                
            
        else:
            raise Exception(datastr, "is not in request_dict. It is not available.")


    def set_mode(self,mode,rate):
        if not mode in mode:
            raise Exception("Modes must be", self.modes)
        self.mode = mode
        self.rate = rate

    def tick(self,sync=False):
        if self.mode == 'best_effort':
            self.mustTick = False
            for rate in range(self.rate):
                print("Middleware Tick!")
                self.robot_simulation.tick()
                if self.send_queue:
                    snd = self.send_queue.pop(0)
                    rStr = self.action_dict[snd][0] + '(' + ','.join(snd[1]) + ')'
                    eval(rStr)
                
            if self.send_queue:
                raise Exception("Send queue not cleared. Too many send commands in 1 cycle.")
                
                
                
                
            

                    
                    
                

        

middleware = morse_middleware()
#middleware.tick()               

#connection = robot_simulation

#def tick():
   # print("tick called")
#    connection.tick()



#def _time():
#    return connection.time()
