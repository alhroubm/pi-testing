import RPi.GPIO as GPIO
import logging
import threading
from threading import Timer

import time
t=None
timerCreated=0
firstTime=1
relay =26
timeout = 20.0
 
def lightsOffTimer():
    global timerCreated
    global relay

    # when this function is called then the motion timer has experired turn off the lights
    print ("turning off light")
    GPIO.output(relay, 0)
    timerCreated = 0

def MOTION(pir):
    global firstTime
    global timerCreated
    global t
    global timeout
    #if(firstTime==1):
    #    print ("First time reached")
    #    firstTime =0;
    #    return

    print ("Motion detected")
    GPIO.output(relay, 1)

    if(timerCreated ==1):
        t.cancel() 
        t = Timer(interval=timeout, function=lightsOffTimer)
        t.start()
    else:
        t = Timer(interval=timeout, function=lightsOffTimer)
        t.start()
        GPIO.output(relay, 1)
    timerCreated = 1


def checkWithMotion(pir):
    #print('Motion: service started')
    #print("Motion Called")
    try:
#        GPIO.add_event_detect(pir, GPIO.RISING, callback=MOTION)
        while 1:
            print("Motion task alive!")
            time.sleep(60)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print ('Motion: Quit')


if __name__ == '__main__':
    timerCreated = 0
    firstTime = 1

    print ("Setting up GPIOs")
    time.sleep(1)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pir = 15
    GPIO.setup(pir, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.add_event_detect(pir, GPIO.RISING, callback=MOTION)#, bouncetime=100)

    GPIO.setmode(GPIO.BCM)
    relay = 26
    GPIO.setup(relay, GPIO.OUT)

    print ("Turning off ligh")
    GPIO.output(relay, 0)

    print ("Using a motion timeout = " + str(timeout))
    thread1 = threading.Thread(target = checkWithMotion, args = (pir,))
    thread1.start()
