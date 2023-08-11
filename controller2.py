from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pwmfreq = 100

# LEFT HAND SIDE
LPWMA = 12
LAIN2 = 18
LAIN1 = 16
LSTBY = 22
LPWMB = 11
LBIN2 = 13
LBIN1 = 15
GPIO.setup(LPWMA, GPIO.OUT) 
GPIO.setup(LAIN2, GPIO.OUT) 
GPIO.setup(LAIN1, GPIO.OUT) 
GPIO.setup(LSTBY, GPIO.OUT) 
GPIO.setup(LPWMB, GPIO.OUT) 
GPIO.setup(LBIN2, GPIO.OUT) 
GPIO.setup(LBIN1, GPIO.OUT)
Lpwma = GPIO.PWM(LPWMA, pwmfreq)
Lpwmb = GPIO.PWM(LPWMB, pwmfreq)
Lpwma.start(0)
Lpwmb.start(0)

# RIGHT HAND SIDE
RPWMA = 29
RAIN2 = 31
RAIN1 = 32
RSTBY = 33
RBIN1 = 36
RBIN2 = 37
RPWMB = 38
GPIO.setup(RPWMA, GPIO.OUT)
GPIO.setup(RAIN2, GPIO.OUT)
GPIO.setup(RAIN1, GPIO.OUT)
GPIO.setup(RSTBY, GPIO.OUT)
GPIO.setup(RBIN1, GPIO.OUT)
GPIO.setup(RBIN2, GPIO.OUT)
GPIO.setup(RPWMB, GPIO.OUT)
Rpwma = GPIO.PWM(RPWMA, pwmfreq)
Rpwmb = GPIO.PWM(RPWMB, pwmfreq)
Rpwma.start(0)
Rpwmb.start(0)

dev = InputDevice('/dev/input/event4')
Lthrottle = 0
Rthrottle = 0
GPIO.output(LSTBY, GPIO.LOW)
GPIO.output(RSTBY, GPIO.LOW)
#while True:
try:
    for event in dev.read_loop():
        if event.type == ecodes.EV_ABS:
            # LEFT
            if event.code == 1:
                #print(event.value)
                if event.value > 138:
                    GPIO.output(LSTBY, GPIO.HIGH)
                    Lthrottle = ((100/127) * event.value) - 100.7874016
                    GPIO.output(LAIN2, GPIO.LOW)
                    GPIO.output(LBIN2, GPIO.LOW)
                    GPIO.output(LAIN1, GPIO.HIGH)
                    GPIO.output(LBIN1, GPIO.HIGH)
                    #Lpwma.ChangeDutyCycle(Lthrottle)
                    #Lpwmb.ChangeDutyCycle(Lthrottle)
                    
                elif event.value < 118:
                    GPIO.output(LSTBY, GPIO.HIGH)
                    Lthrottle = ((-100/128) * event.value)  + 100
                    GPIO.output(LAIN2, GPIO.HIGH)
                    GPIO.output(LBIN2, GPIO.HIGH)
                    GPIO.output(LAIN1, GPIO.LOW)
                    GPIO.output(LBIN1, GPIO.LOW)
                    #Lpwma.ChangeDutyCycle(Lthrottle)
                    #Lpwmb.ChangeDutyCycle(Lthrottle)
                    
                elif 118 <= event.value <= 138:
                    Lthrottle = 0
                    #Lpwma.ChangeDutyCycle(Lthrottle)
                    #Lpwmb.ChangeDutyCycle(Lthrottle)
                    
            # RIGHT
            elif event.code == 4:
                #print(event.value)
                if event.value > 138:
                    GPIO.output(RSTBY, GPIO.HIGH)
                    Rthrottle = ((100/127) * event.value) - 100.7874016
                    GPIO.output(RAIN1, GPIO.LOW)
                    GPIO.output(RBIN1, GPIO.LOW)
                    GPIO.output(RBIN2, GPIO.HIGH)
                    GPIO.output(RAIN2, GPIO.HIGH)
                    #Rpwma.ChangeDutyCycle(Rthrottle)
                    #Rpwmb.ChangeDutyCycle(Rthrottle)
                    
                elif event.value < 118:
                    GPIO.output(RSTBY, GPIO.HIGH)
                    Rthrottle = ((-100/128) * event.value)  + 100
                    GPIO.output(RAIN1, GPIO.HIGH)
                    GPIO.output(RBIN1, GPIO.HIGH)
                    GPIO.output(RBIN2, GPIO.LOW)
                    GPIO.output(RAIN2, GPIO.LOW)
                    #Rpwma.ChangeDutyCycle(Rthrottle)
                    #Rpwmb.ChangeDutyCycle(Rthrottle)
                    
                elif 118 <= event.value <= 138:
                    Rthrottle = 0
                    #Rpwma.ChangeDutyCycle(Rthrottle)
                    #Rpwmb.ChangeDutyCycle(Rthrottle)
                
        #print("(" + str(Lthrottle) + ", " + str(Rthrottle) + ")")
            Lpwma.ChangeDutyCycle(Lthrottle)
            Lpwmb.ChangeDutyCycle(Lthrottle)
            Rpwma.ChangeDutyCycle(Rthrottle)
            Rpwmb.ChangeDutyCycle(Rthrottle)
            
except KeyboardInterrupt():
    GPIO.output(LSTBY, GPIO.LOW)
    GPIO.output(RSTBY, GPIO.LOW)
    GPIO.cleanup()
        
