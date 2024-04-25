import netifaces as ni
import nmap
import ipaddress
import urllib.request
import requests
import json
import subprocess
from flask import *
import os
import time
import logging
import docker
import configparser
import threading
from flask import *
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

pir_state = False

@app.route('/pir')
def test():
    return pir_state

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 15
GPIO.setup(PIR_PIN, GPIO.IN)

print('Starting up the PIR Module (click on STOP to exit)')
time.sleep(1)
print ('Ready')

def flaskThread():
    global controllerPort
    print ("flask thread started")
    app.run(host= '0.0.0.0',port=5005)

def checkNeighbours():

    global servicePort
    global logger
    
    neighbours = set()
    ni.ifaddresses('wlan0')
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    netmask = ni.ifaddresses('wlan0')[ni.AF_INET][0]['netmask']
    gateway = ni.gateways()['default'][ni.AF_INET][0]
    print("IP            "+ip)
    print("Netaask       "+netmask)
    print("Gateway IP    "+gateway)
    
    # cidr e.g. 192.168.43.0/24
    net = str(ipaddress.ip_network(ip+"/"+netmask,strict=False))
    print("Subnet        "+net)

    # getting all ip addresses in the subnet
    nm = nmap.PortScanner()
    print ("starting port scan")
    nm.scan(hosts=net, arguments='-sn -sP -PE -PA21,23,80,3389')
    print("port scan cmpleted")
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

    for host, status in hosts_list:
        print ('Checking on ' + host)

    print('+++++')

    for host, status in hosts_list:
        print ('Checking on ' + host)
        if status=='up' and host!=gateway and host!=ip:
            print("Other IPs     "+host)
            try:
                if urllib.request.urlopen("http://"+host+":"+str(servicePort)+"/battery").getcode()==200:
                    logger.info('Neighbour:'+ str(host)+' is active')
                    print ('Neighbour:'+ str(host)+' is active')
                    neighbours.add(host)
                else:
                    print ('Neighbour:'+ str(host)+' is down')
            except:
#                logger.info('Neighbour:'+ str(host)+' is down')
                print ('Neighbour:'+ str(host)+' is down')
                
    return neighbours
    
if __name__ == "__main__":
#    logger = logging.getLogger('dev')
#    logger.setLevel(logging.INFO)
#    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

#    fileHandler = logging.FileHandler('PiController.log')
#    fileHandler.setFormatter(formatter)
#    fileHandler.setLevel(logging.INFO)

#    consoleHandler = logging.StreamHandler()
#    consoleHandler.setFormatter(formatter)
#    consoleHandler.setLevel(logging.INFO)

#    logger.addHandler(fileHandler)
#    logger.addHandler(consoleHandler)
    
    time.sleep(2)
        
    controllerPort=8000
    servicePort=5000
    
    #thread1 = threading.Thread(target = flaskThread, args = ())
    #thread1.start()
    #time.sleep(1)


    while True:
        if GPIO.input(PIR_PIN):
            print('Motion Detected')
            pir_state = True
        #checkNeighbours()
        time.sleep(1)
        #pir_state = False
