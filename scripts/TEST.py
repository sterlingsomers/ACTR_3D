from pymorse import Morse
import time

with Morse() as simu:
    count = 0
    while True:
        count+=1
        #simu.robot.GeometricCamerav1.scan_image()
        #print("ASDF")
        #simu.robot.GeometricCamerav1.scan_image()
        #print("JKL;")
        print(simu.time())
        #print(simu.time(), "again")
        time.sleep(1)
        print("QWERTY")
        print(count)
    #print(simu.time())
        simu.tick()
