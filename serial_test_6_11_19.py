from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.text import LabelBase
#font file needs to be in the folder
LabelBase.register(name="Dodger", fn_regular= "dodger3condital.ttf")
LabelBase.register(name="Roboto", fn_regular= "RobotoSlab-Regular.ttf")

import serial 
import threading
import serial.tools.list_ports
import pyglet
import multiprocessing
from apscheduler.schedulers.background import BackgroundScheduler
import os
 
SERIAL_PORT = ""

def port_listB():
    try: 
        comlist = serial.tools.list_ports.comports()
        connected = []
        for element in comlist:
            connected.append(element.device)
            print("Connected COM ports: " + str(connected))
            label2.text = "Connected COM ports: " + str(connected)
    except:
        label2.text = 'serial problem'
        print('serial problem') 
        
button = [" X "," A "," B "," Y "," Lb "," Rb "," Lt "," Rt "," Back "," Start "," Hat_1 "," Hat_2 "] 


        
def joystick():  
    try:
        while True:
            joysticks = pyglet.input.get_joysticks() 
            joystick = joysticks[0]
            joystick.open()
            #print(joystick.event_types)
            #joystick.register_event_type('on_joyaxis_motion',)
            #for k, v in vars(joystick).items():
                #print (k, v)
                
            if not int(joystick.x) == 0:
                label10.text = 'x'+str(joystick.x)
            if not int(joystick.y) == 0:
                label10.text = 'y'+str(joystick.y)  
            if not int(joystick.z) == 0:
                label10.text = 'z'+str(joystick.z)
            if not int(joystick.hat_x) == 0:
                label10.text = 'hx'+str(joystick.hat_x)  
            if not int(joystick.hat_y) == 0:
                label10.text = 'hy'+str(joystick.hat_y) 
            for i in range(len(joystick.buttons)):    
                if not (joystick.buttons[i]) == False:
                    label10.text = str(button[i]) 
                
            
            #Don't like this but it's the only way I got it to behave
            #For the mac the joystick needs to be in D
            #x and y on the hats are discrete
            #green light on the controller needs to be on and solid
            #if the joystick connection fails the program has to be restarted
            
            label5.text = "Direction Pad  x  "+str(joystick.x)+"  y  "+str(joystick.y)+"\n"+"Hats  x  "+str(joystick.hat_x)+"  y  "+str(joystick.hat_y)+"  z  "+str(joystick.z)+"\n"+"Buttons  " + str(button[0]) + str(joystick.buttons[0]) + str(button[1]) + str(joystick.buttons[1])+ str(button[2]) + str(joystick.buttons[2])+ str(button[3]) + str(joystick.buttons[3])+ str(button[4]) + str(joystick.buttons[4])+ str(button[5]) + str(joystick.buttons[5])+"\n"+ str(button[6]) + str(joystick.buttons[6])+ str(button[7]) + str(joystick.buttons[7])+ str(button[8]) + str(joystick.buttons[8])+ str(button[9]) + str(joystick.buttons[9])+ str(button[10]) + str(joystick.buttons[10])+ str(button[11]) + str(joystick.buttons[11])
            
            #writing to the arduino will have to be handled with the apscheduler
            
    except:
        print('Joystick Failed')
        label5.text = 'Joystick Failed'
                
def port_contB():
    if SERIAL_PORT != "":
        try:
            global input_queue
            global output_queue
            global sp
            input_queue = multiprocessing.Queue()
            output_queue = multiprocessing.Queue()
            sp = SerialProcess(output_queue, input_queue) 
            sp.daemon = True
            sp.start()
            label3.text = 'Connected'
            print('connected')  
        except:
            label3.text = 'Serial Problem'
            print('serial problem')
            print(SERIAL_PORT)
    else:
        label3.text = 'Input Serialport Address'
        print('Input Serialport Address')
        
def arduino(self): 
        global sched
        sched = BackgroundScheduler(dameon = True)
        sched.add_job(self.checkQueue,'interval', seconds = 1)
        try:
            sched.start()
            label6.text = "Arduino Streaming"
        except:
            label6.text = "Streaming Failed"
            print("Streaming Failed")        
        

    
class SerialTestWindow(FloatLayout): 
    def term(self):
        sp.terminate()
        os._exit(-1)
    
    def send_command(self, value):
        #writing to the arduino will have to be handled with the apscheduler
        pass
        #self.cmd_result += 'Output: {}\n'.format(self.cmd_send.text)
        #output_queue.put(self.cmd_send.text.encode('ascii'))
        #output_queue.put(label7.text)
        #self.cmd_send.text = ''
        #cmd_send = ""
        #self.cmd_send.focus = True
        
    def checkQueue(self):
        if not input_queue.empty():
            global label9
            label9 = self.ids['l9']
            label9.text = str(input_queue.get())
            output_queue.put(label10.text)
        #this is handled by the apscheduler 
        
    def writeQueue(x):
        pass
            #global label10
            #label10.text = str(output_queue.put())
            #label10.text = str(joystick.get_controls())
        
        #this is handled by the apscheduler    
            
    
    def port_list(self):
        global label2
        label2 = self.ids['l2']
        t1 = threading.Thread(target=port_listB)
        t1.daemon = True
        t1.start()
                
    def port_cont(self):
        global label3
        label3 = self.ids['l3']
        t2 = threading.Thread(target=port_contB)
        t2.daemon = True
        t2.start()
        
    def got_port(self):
        global SERIAL_PORT
        SERIAL_PORT = self.ids['l4'].text
        
    def got_joystick(self):
        global label5
        global label10
        label5 = self.ids['l5']
        label10 = self.ids['l10']
        t3 = threading.Thread(target=joystick)
        t3.daemon = True
        t3.start()
          
    def got_data(self):
        global label6
        label6 = self.ids['l6']
        t4 = threading.Thread(target=arduino(self))
        t4.daemon = True
        t4.start()
        
class SerialProcess(multiprocessing.Process):
    def __init__ (self, input_queue, output_queue):
        try:
            multiprocessing.Process.__init__(self)
            self.input_queue = input_queue
            self.output_queue = output_queue
            self.sp = serial.Serial(SERIAL_PORT, 115200, timeout=1)
        except:
            label3.text = 'serial problem'
            print('serial problem')
            print(SERIAL_PORT)
        
    def close(self):
        self.sp.close()
        
    def writeSerial(self, data1):
        try:
            return self.sp.write(data1)
        except:
            pass
        
    def readSerial(self):
        try:
            return self.sp.readline()
        except:
            pass
    
    def run(self):
        self.sp.flushInput()
        
        while True:
            if not self.input_queue.empty():
                try:
                    data1 = self.input_queue.get()
                    self.writeSerial(data1)
                except:
                    pass
                
                
            if self.sp.inWaiting() > 0:
                try:
                    data2 = self.readSerial()
                    self.output_queue.put(data2)
                except:
                    pass
                
                    			
class Serial_test_6_7_19App(App):
    def build(self):
        return SerialTestWindow()
    			
if __name__=='__main__':
	Serial_test_6_7_19App().run()
	
	