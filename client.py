# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 23:55:09 2018

@author: Jhon GIl Sepulveda
"""

import websocket
try:
    import thread
except ImportError:
    import _thread as thread

import sys
import threading
import json
import ev3dev.ev3 as ev3

from random import randint

server = "192.168.43.106"
port = "8095"

large_motor1 = ev3.LargeMotor('outA')
large_motor2 = ev3.LargeMotor('outD')
medium_motor = ev3.LargeMotor('outC')

# ir_sensor = ev3.InfraredSensor()
# color_sensor = ev3.ColorSensor()
# touch_sensor = ev3.TouchSensor()

sensor_stop = threading.Event()

def on_message(ws, message):
    print(message)
    try:
        state = json.loads(message)
        if state['type'] == 'motor':
            if '11' in state:
                # print("Large motor 1: ", state['11'])
                large_motor1.run_forever(speed_sp = state['11'])
            if '12' in state:
                # print("Large motor 2: ", state['12'])
                large_motor2.run_forever(speed_sp = state['12'])
            if 'm' in state:
                #print("Medium motor: ", state['m'])
                medium_motor.run_forever(speed_sp = state['m'])
        if state['type'] == 'speak':
            # print("Speak: ", state['text'])
            ev3.Sound.speak(state['text']).wait()            
        if state['type'] == 'stop':
            print("--- Stopping process ---")
            sensor_stop.set()
            exit()
    except:
        print("Failed handling commands: ", sys.exc_info()[0])

def on_error(ws, error):
    print("--- Connection error, closing ---")
    print("Error: ", error)
    sensor_stop.set()

def on_close(ws):
    print("--- Connection close ---")
    sensor_stop.set()

def on_open(ws):
    print("-- Connected to Socket ---")
    t = threading.Thread(target = process_input, args = (ws, sensor_stop))
    t.start()

def process_input(ws, stop):
    while not stop.wait(0.1):
        sensors = {
            "type": "sensor",
            "ir": randint(0, 20), # ir_sensor.value(),
            "color": randint(0, 20), # color_sensor.value()
            "touch": randint(0, 20) # touch_sensor.value()
        }
        ws.send(json.dumps(sensors))
    # print("WebSocket: ", ws)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://"+ server +":" + port + "/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()