import pygame
import math
import RPi.GPIO as GPIO
import cv2
from picamera2 import Picamera2

# Rover project start: 05 - 25 - 2023

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pwmfreq = 100

# Pi Cam
piCam=Picamera2()
piCam.preview_configuration.main.size=(1280,720)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

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

# Pygame screen stuff
pygame.init()
SCREEN_SIZE = 600
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
S2 = int(round(SCREEN_SIZE/2))
S16 = int(round(SCREEN_SIZE * (1/16)))
S1516 = int(round(SCREEN_SIZE * (15/16)))
S02 = int(round(SCREEN_SIZE*0.28125))
S07 = int(round(SCREEN_SIZE*0.71875))

pygame.display.set_caption("Rover Control")
grey_color = (40, 40, 40)
green_color = (102, 255, 102)

joystick_radius = 15
joystick_color = green_color
joystick_position = (int(SCREEN_SIZE / 2), int(SCREEN_SIZE / 2))
dragging = False

# This function bounds the joystick inside the diamond for throttle calculations
def angler():
    new_pos = pygame.mouse.get_pos()
    adjusted_x = new_pos[0] - SCREEN_SIZE / 2
    adjusted_y = -(new_pos[1] - SCREEN_SIZE / 2)
    angle = math.degrees(math.atan2(adjusted_y, adjusted_x))
    position = new_pos
    mag = (adjusted_x ** 2 + adjusted_y ** 2) ** 0.5
    if 0 < angle <= 90:
        bounded_mag = (SCREEN_SIZE * (7 / 16) * math.sin(math.pi / 4)) / (math.sin(math.radians(135 - angle)))
        if mag > bounded_mag:
            position = [int(round(SCREEN_SIZE / 2 + (bounded_mag * math.cos(math.radians(angle))))),
                        int(round(SCREEN_SIZE / 2 - (bounded_mag * math.sin(math.radians(angle)))))]
    elif 90 < angle <= 180:
        angle -= 90
        bounded_mag = ((SCREEN_SIZE * (7 / 16)) * math.sin(math.pi / 4)) / (math.sin(math.radians(135 - angle)))
        if mag > bounded_mag:
            position = [int(round(SCREEN_SIZE / 2 - (bounded_mag * math.sin(math.radians(angle))))),
                        int(round(SCREEN_SIZE / 2 - (bounded_mag * math.cos(math.radians(angle)))))]
    elif -180 <= angle < -90:
        angle = 180 + angle
        bounded_mag = (SCREEN_SIZE * (7 / 16) * math.sin(math.pi / 4)) / (math.sin(math.radians(135 - angle)))
        if mag > bounded_mag:
            position = [int(round(SCREEN_SIZE / 2 - (bounded_mag * math.cos(math.radians(angle))))),
                        int(round(SCREEN_SIZE / 2 + (bounded_mag * math.sin(math.radians(angle)))))]
    elif -90 <= angle <= 0:
        angle *= -1
        bounded_mag = (SCREEN_SIZE * (7 / 16) * math.sin(math.pi / 4)) / (math.sin(math.radians(135 - angle)))
        if mag > bounded_mag:
            position = [int(round(SCREEN_SIZE / 2 + (bounded_mag * math.cos(math.radians(angle))))),
                        int(round(SCREEN_SIZE / 2 + (bounded_mag * math.sin(math.radians(angle)))))]
    return position


# This function calculates the throttle for each side using joystick position
def throttle_calculator(x, y):
    right_hand_throttle = ((-114.2857143/SCREEN_SIZE) * x) - ((228.5714286/SCREEN_SIZE)*y) + 171.4285714
    left_hand_throttle = ((114.2857143 / SCREEN_SIZE) * x) - ((228.5714286 / SCREEN_SIZE) * y) + 57.14285713

    throttle_values = [math.ceil(left_hand_throttle), math.ceil(right_hand_throttle)]
    #print("(" + str(throttle_values[0]) + ", " + str(throttle_values[1]) + ")")
    return throttle_values


running = True
while running:
    screen.fill(grey_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if ((joystick_position[0] - mouse_pos[0]) ** 2 + (
                    joystick_position[1] - mouse_pos[1]) ** 2) ** 0.5 <= joystick_radius:
                dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            joystick_position = (int(SCREEN_SIZE / 2), int(SCREEN_SIZE / 2))

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                joystick_position = angler()

    throttle = throttle_calculator(joystick_position[0], joystick_position[1])
    
    if throttle[0] > 0:
        if not GPIO.input(LSTBY):
            GPIO.output(LSTBY, GPIO.HIGH) # standby off
            
        GPIO.output(LAIN2, GPIO.HIGH)
        GPIO.output(LBIN2, GPIO.HIGH)
        GPIO.output(LAIN1, GPIO.LOW)
        GPIO.output(LBIN1, GPIO.LOW)
        Lpwma.ChangeDutyCycle(throttle[0])
        Lpwmb.ChangeDutyCycle(throttle[0])
    
    elif throttle[0] < 0:
        if not GPIO.input(LSTBY):
            GPIO.output(LSTBY, GPIO.HIGH) # standby off
            
        GPIO.output(LAIN2, GPIO.LOW)
        GPIO.output(LBIN2, GPIO.LOW)
        GPIO.output(LAIN1, GPIO.HIGH)
        GPIO.output(LBIN1, GPIO.HIGH)
        Lpwma.ChangeDutyCycle(abs(throttle[0]))
        Lpwmb.ChangeDutyCycle(abs(throttle[0]))
        
    elif throttle[0] == 0:
        GPIO.output(LSTBY, GPIO.LOW)
        
    if throttle[1] > 0:
        if not GPIO.input(RSTBY):
            GPIO.output(RSTBY, GPIO.HIGH) # standby off
            
        GPIO.output(RAIN1, GPIO.HIGH)
        GPIO.output(RBIN1, GPIO.HIGH)
        GPIO.output(RBIN2, GPIO.LOW)
        GPIO.output(RAIN2, GPIO.LOW)
        Rpwma.ChangeDutyCycle(throttle[1])
        Rpwmb.ChangeDutyCycle(throttle[1])
        
    elif throttle[1] < 0:
        if not GPIO.input(RSTBY):
            GPIO.output(RSTBY, GPIO.HIGH) # standby off
        
        GPIO.output(RAIN1, GPIO.LOW)
        GPIO.output(RBIN1, GPIO.LOW)
        GPIO.output(RBIN2, GPIO.HIGH)
        GPIO.output(RAIN2, GPIO.HIGH)
        Rpwma.ChangeDutyCycle(abs(throttle[1]))
        Rpwmb.ChangeDutyCycle(abs(throttle[1]))
        
    elif throttle[1] == 0:
        GPIO.output(RSTBY, GPIO.LOW)
        
    pygame.draw.line(screen, green_color, (S2, S16), (S2, S1516))
    pygame.draw.line(screen, green_color, (S16, S2), (S1516, S2))
    pygame.draw.line(screen, green_color, (S02, S02), (S07, S07))
    pygame.draw.line(screen, green_color, (S02, S07), (S07, S02))
    pygame.draw.lines(screen, green_color, True, ([S2, S16], [S1516, S2], [S2, S1516], [S16, S2]), 5)
    
    pygame.draw.circle(screen, joystick_color, joystick_position, joystick_radius)
    pygame.display.flip()
    
    frame=piCam.capture_array()
    cv2.imshow("Rover Live Feed", frame)
    if cv2.waitKey(1)==ord('q'):
        break

print("Rover Shutdown")
GPIO.output(LSTBY, GPIO.LOW)
GPIO.output(RSTBY, GPIO.LOW)
GPIO.cleanup()
cv2.destroyAllWindows()
pygame.quit()
