from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.text import LabelBase
#font file needs to be in the folder
LabelBase.register(name="Dodger", fn_regular= "dodger3condital.ttf")
LabelBase.register(name="Roboto", fn_regular= "RobotoSlab-Regular.ttf")
from pudb import set_trace;
import serial 
import threading
import serial.tools.list_ports
import pyglet
import multiprocessing
from apscheduler.schedulers.background import BackgroundScheduler
import os
 
SERIAL_PORT = ""
sched = BackgroundScheduler(dameon = True)


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
        
button = [" X "," A "," B "," Y "," Lb "," Rb "," Lt ",
          " Rt "," Back "," Start "," Hat_1 "," Hat_2 "] 


        
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
        
def port_contC(): 
    #set_trace(paused=True)
    if SERIAL_PORT != "":
        global newsp
        try: 
            newsp = serial.Serial(SERIAL_PORT, 115200, timeout=1)
            label3.text = 'Connected'
            print('Connected to serial port')
        
        except: 
            print('Cant connect to serial port')
            label3.text = 'Serial Problem'
    else:
        label3.text = 'Input Serialport Address'      
            
def serial_write():
    if not label10.text =="Data":
        b = label10.text.encode('utf-8')
        newsp.write(b)
        label10.text = "Data"
        label12.text = str(newsp.out_waiting)
        
        
def serial_read():
    label9.text = str(newsp.read(10))
    label11.text = str(newsp.in_waiting)
    
        
def arduinoB():
    try:
        global sched
        sched.add_job(serial_write,'interval', seconds = .15)
        sched.add_job(serial_read,'interval', seconds = .15)
        sched.start()
        label6.text = "Serial Streaming"
    except:
        label6.text = "Job Failed"
           
class SerialTestWindow(FloatLayout): 
    
    def term(self):
        newsp.close()
        sched.shutdown(wait=False)        
        os._exit(-1)
      
    def port_list(self):
        global label2
        label2 = self.ids['l2']
        t1 = threading.Thread(target=port_listB)
        t1.daemon = True
        t1.start()
                
    def port_cont(self):
        global label3
        label3 = self.ids['l3']
        t2 = threading.Thread(target=port_contC)
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
        global label9
        global label10
        global label11
        global label12
        label6 = self.ids['l6']
        label9 = self.ids['l9']
        label10 = self.ids['l10']
        label11 = self.ids['l11']
        label12 = self.ids['l12']
        t4 = threading.Thread(target=arduinoB())
        t4.daemon = True
        t4.start()        
                    			
class Serial_test_6_12_19_mikeApp(App):
    def build(self):
        return SerialTestWindow()
    			
if __name__=='__main__':
	Serial_test_6_12_19_mikeApp().run()
	
	