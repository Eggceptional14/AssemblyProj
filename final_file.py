import speech_recognition as sr
import pyttsx3
import RPi.GPIO as GPIO  
import tkinter
import subprocess
import ledControllerApp as lca

GPIO.setmode(GPIO.BCM)
r = sr.Recognizer()

GPIO.setup( 15, GPIO.OUT )
GPIO.setup( 23, GPIO.OUT )
GPIO.setup( 24, GPIO.OUT )
GPIO.setup( 25, GPIO.OUT )

pwm = GPIO.PWM( 15, 50 )
red = GPIO.PWM( 23, 50 )
blue = GPIO.PWM( 24, 50 )
green = GPIO.PWM( 25, 50 )

filename = "command_list.txt"

def load_command():
    temp = {}
    file = open( filename, "r")
    lines = file.readlines()
    for line in lines:
        line = line.split(",")
        print( line )
        temp[line[0]] = [line[1],line[2],line[3][:-1]]
    file.close()
    return temp    

def set_light( light ):
    red.ChangeDutyCycle( 100 - light[0])
    green.ChangeDutyCycle( 100 - light[1])
    blue.ChangeDutyCycle( 100 - light[2])

if (__name__ == "__main__" ):
    color = load_command()
    pwm.start(0)
    red.start(0)
    green.start(0)
    blue.start(0)
    pwm.ChangeDutyCycle( 100 )
    
    light = [100, 100, 100]
    savecolor = [100,100,100]
    
    lca.call_ui()
    color = load_command()

    while ( True ):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise( source2, duration = 0.2)
                print( "Speak" )
                audio2 = r.listen(source2)
                request = r.recognize_google(audio2)
                request = request.upper()
                print(  request )
            if ( request == "END" ):
                subprocess.Popen( 'sudo ./light_control/light_off', shell = True)
                break
            if ( request == "OFF"):
                subprocess.Popen( 'sudo ./light_control/light_off', shell = True)
            elif ( request == "ON" ):
                subprocess.Popen( 'sudo ./light_control/light_on', shell = True)
            elif ( request == "BRIGHT" ):
                light = savecolor
                set_light(light)

            elif ( request == "DIM" ):
                temp = [light[0],light[1],light[2]]
                for i in range( len(light) ):
                    if light[i] > 0 and light[i] <= 25:
                        temp = [0,0,0]
                        break
                    temp[i] = max( 0, light[i] - 25 )
                light = temp
                set_light(light)
            elif ( request == "CUSTOMIZE"):
                lca.call_ui()
                color = load_command()
                
            elif request in color.keys() :
                request = color[request]
                light = [int(request[0]), int(request[1]), int(request[2])]
                savecolor = [int(request[0]), int(request[1]), int(request[2])]
                set_light(light)
                print(light)
            else :
                print ("Unknown command, please try again!" )
        except sr.RequestError as e:
            print( e )
        except sr.UnknownValueError:
            print( "Unknown Speech" )
                
    GPIO.cleanup()

