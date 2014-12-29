#from .morseconnection import *
#import morseconnection
import time


class morse_middleware():
    '''The middleware to handle the connection between ACT-R and Morse.'''
    
    def __init__(self):
        from .morseconnection import robot_simulation
            #.robot_simulation
        if robot_simulation == None:
            raise Exception("pymorse was not detected, or connection was not successful.")

        self.robot_simulation = robot_simulation
        self.mustTick = False
        self.active=False
        self.modes = ['best_effort']
        self.send_dict = {'set_speed':True,
                        'move_forward':False,
                        'set_rotation':False} #{function_name:blocking?}

        self.request_dict = {'scan_imageD':True,
                'getScreenVector':True,
                'cScan':True,
                'get_time':True,
                'xScan':True}
            
        self.action_dict = {'scan_imageD':['self.robot_simulation.robot.GeometricCamerav1', '.scan_imageD'],
				'set_speed':['self.robot_simulation.robot','.set_speed'],
                'move_forward':['self.robot_simulation.robot','.move_forward'],
                'set_rotation':['self.robot_simulation.robot.armature','.set_rotation'],
                'getScreenVector':['self.robot_simulation.robot.GeometricCamerav1', '.getScreenVector'],
                'cScan':['self.robot_simulation.robot.GeometricCamerav1', '.cScan'],
                'xScan':['self.robot_simulation.robot.GeometricCamerav1', '.xScan']}

        self.danger_list = ['get_time']
        self.modules_in_use = {}
        #{function_name:['absolute path to function', ['args', 'list']]}
#    def set_speed(self,speed=0.01):
#        '''Move forward @speed in m/s'''
#        x = robo.set_speed(speed).result()
        self.send_queue = [] #contains [[datastr,argslist],[datastr,argslist]]
        self.request_queue = []
        
    def send(self, datastr, argslist):
        print("Trying to send", datastr)
        if not type(argslist) == list:
            raise Exception("arglist parameter must be a list")
        if not all(isinstance(x,str) for x in argslist):
            raise Exception("All arguments have to be strings")
        if not datastr in self.send_dict:
            raise Exception(datastr + " is not in send_dict. Command does not exist or must be added.")
        if self.mustTick:#Something has blocked
            self.send_queue.append([datastr,argslist])
        else:
            if self.send_dict[datastr]: #it is blocking
                pass
            else: #if it's not blocking, we need to add it's location to a list, and check if it is already in the list
                if self.action_dict[datastr][0] in self.modules_in_use:
                    raise Exception("Module " + self.action_dict[datastr][0] + " is already in use this cycle by " 
                    + self.modules_in_use[self.action_dict[datastr][0]])
                else:
                    self.modules_in_use[self.action_dict[datastr][0]] = datastr #set it as in use
                    #print(self.modules_in_use)
                    rStr = self.action_dict[datastr][0] + self.action_dict[datastr][1] + '(' + ','.join(argslist) + ')'
                    #print(rStr)
                    eval(rStr)
                                
            
#    def send(self, datastr, argslist):
#        '''send a command, no response required. If a blocking command, pushed to next tick cycle.'''
#        if not type(argslist) == list:
#            raise Exception("argslist parameter must be a list")
#        if not all(isinstance(x,str) for x in argslist):
#           raise Exception("All arguments have to be strings")
#        if datastr in self.send_dict:
#            if not self.mustTick:
#            #Can run it now, but must block future
#                if not self.send_dict[datastr]:
#                    #It is non-blocking
#                    rStr = self.action_dict[datastr][0] + '(' + ','.join(argslist) + ')'
#                    eval(rStr)
#                else:
#                    #it is blocking
#                    self.mustTick = True
#                    rStr = self.action_dict[datastr][0] + '(' + ','.join(argslist) + ')'
#                    eval(rStr)
#                    #no return, it's a command being sent. Assume it worked.
#            else:
#                if self.mode == 'best_effort':
#                    print("!!!!!! Adding", datastr, "to QUEUE")
#                    self.send_queue.append([datastr,argslist])
#                else:
#                    raise Exception(datastr + " dropped. Use best_effort mode to use multiple blocking sends.")
#
#
#        else:
#            raise Exception(datastr + " is not in send_dict. It is not available.")
                    
        
            
        
        
    def request(self, datastr, argslist):
       
        print("Trying to request", datastr)
        result = None
        if not type(argslist) == list:
            raise Exception("argslist parameter must be a list")
        if not all(isinstance(x,str) for x in argslist):
            raise Exception("All arguments have to be strings")
        if not datastr in self.request_dict:
            raise Exception(datastr + " is not in request_dict. Command does not exist or must be added.")
        if self.mustTick:
            raise Exception("Blocking request already made.")#make something more informative        
        self.mustTick = True
        print("Sending...", self.action_dict[datastr][1], argslist)
        rStr = self.action_dict[datastr][0] + self.action_dict[datastr][1] + '(' + ','.join(argslist) + ').result()'
        result = eval(rStr)
        print("Recieved", result)
        #if 'return' in dir(result):
        #    result = result.result()
        while result == None:
           time.sleep(0.0001)
        return result


#    def request(self, datastr, argslist):
#        '''Request data. Most actions require a tick. Parallel actions will occur in random order, in following cycles.'''
#        if not type(argslist) == list:
#            raise Exception("argslist parameter must be a list")
#        if not all(isinstance(x,str) for x in argslist):
#            raise Exception("All arguments have to be strings")
#        if self.mustTick:#blocking command send/request has been made already
#            raise Exception("A blocking even has already occured.")#
#
#        if datastr in self.request_dict:
#            if self.request_dict[datastr]:#is it blocking?
#                if self.mustTick:#already blocking?
#                    raise Exception("A blocking event has already occured")
#                self.mustTick = True
#                rStr = self.action_dict[datastr][0] + '(' + ','.join(argslist) + ')'
#                result = eval(rStr)
#                if 'return' in dir(result):
#                    result = result.result()
#                return result #must be returned right away because it's a request
#            else:
#                #no mustTick, it's not blocking
#                rStr = self.action_dict[datastr][0] + '(' + ','.join(argslist) + ')'
#                result = eval(rStr)
#                if 'return' in dir(result):
#                    result = result.result()
#                return result
#                
#                
#            
#        else:
#            raise Exception(datastr, "is not in request_dict. It is not available.")


    def set_mode(self,mode,rate):
        if not mode in mode:
            raise Exception("Modes must be", self.modes)
        self.mode = mode
        self.rate = rate

    def tick(self,sync=False):
        #eimport time
        if self.mode == 'best_effort':
            self.mustTick = False
            self.modules_in_use = {}
            for rate in range(self.rate):
                print("Middleware tick!")
                self.robot_simulation.tick()
                if self.send_queue:
                    print("Popping send queue")
                    snd = self.send_queue.pop(0)
                    self.send(snd[0],snd[1])
            if self.send_queue:
                raise Exception("Send queue not clear. Too many commands per cycle.")
#    def tick(self,sync=False):
#        if self.mode == 'best_effort':
#            self.mustTick = False
#            for rate in range(self.rate):
#                print("Middleware Tick!")
#                self.robot_simulation.tick()
#                if self.send_queue:
#                    snd = self.send_queue.pop(0)
#                    print(self.action_dict[snd[0]], "!@#$!@#$", snd[1])
#                    rStr = self.action_dict[snd[0]][0]  +'(' + ','.join(snd[1]) + ')'
#                    eval(rStr)
#                
#            if self.send_queue:
#                raise Exception("Send queue not cleared. Too many send commands in 1 cycle.")
                
                
                
                
            

                    
                    
                

        

middleware = None#morse_middleware()
#middleware.tick()               

#connection = robot_simulation

#def tick():
   # print("tick called")
#    connection.tick()



#def _time():
#    return connection.time()
