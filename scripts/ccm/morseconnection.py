#from pymorse import Morse


try:
    from pymorse import Morse
except ImportError:
    raise Exception("pymorse not properly installed")

robot_simulation = Morse()




