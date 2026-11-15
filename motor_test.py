import RPi.GPIO as GPIO
import time

# GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# First L298N (Motors 1 & 2)
ENA1 = 18  # PWM for Motor 1 & 2
ENB1 = 19
IN1_1 = 17
IN2_1 = 27
IN3_1 = 22
IN4_1 = 23

# Second L298N (Motors 3 & 4)
ENA2 = 12  # PWM for Motor 3 & 4
ENB2 = 16
IN1_2 = 5
IN2_2 = 6
IN3_2 = 13
IN4_2 = 26

# Setup GPIO pins
GPIO.setup([ENA1, ENB1, IN1_1, IN2_1, IN3_1, IN4_1, ENA2, ENB2, IN1_2, IN2_2, IN3_2, IN4_2], GPIO.OUT)

# Setup PWM
pwm1A = GPIO.PWM(ENA1, 1000)  # PWM at 1kHz
pwm1B = GPIO.PWM(ENB1, 1000)
pwm2A = GPIO.PWM(ENA2, 1000)
pwm2B = GPIO.PWM(ENB2, 1000)

# Start PWM with 0% duty cycle (motors off)
pwm1A.start(0)
pwm1B.start(0)
pwm2A.start(0)
pwm2B.start(0)

def set_motor(speed, direction):
    """
    Controls all 4 motors:
    - speed (0-100): PWM duty cycle
    - direction: "forward", "backward", or "stop"
    """
    if direction == "forward":
        # First L298N
        GPIO.output(IN1_1, GPIO.HIGH)
        GPIO.output(IN2_1, GPIO.LOW)
        GPIO.output(IN3_1, GPIO.HIGH)
        GPIO.output(IN4_1, GPIO.LOW)
        # Second L298N
        GPIO.output(IN1_2, GPIO.HIGH)
        GPIO.output(IN2_2, GPIO.LOW)
        GPIO.output(IN3_2, GPIO.HIGH)
        GPIO.output(IN4_2, GPIO.LOW)
    
    elif direction == "backward":
        GPIO.output(IN1_1, GPIO.LOW)
        GPIO.output(IN2_1, GPIO.HIGH)
        GPIO.output(IN3_1, GPIO.LOW)
        GPIO.output(IN4_1, GPIO.HIGH)
        GPIO.output(IN1_2, GPIO.LOW)
        GPIO.output(IN2_2, GPIO.HIGH)
        GPIO.output(IN3_2, GPIO.LOW)
        GPIO.output(IN4_2, GPIO.HIGH)
    
    else:  # Stop motors
        GPIO.output([IN1_1, IN2_1, IN3_1, IN4_1, IN1_2, IN2_2, IN3_2, IN4_2], GPIO.LOW)

    # Set speed
    pwm1A.ChangeDutyCycle(speed)
    pwm1B.ChangeDutyCycle(speed)
    pwm2A.ChangeDutyCycle(speed)
    pwm2B.ChangeDutyCycle(speed)

try:
    print("Motors moving forward")
    set_motor(50, "forward")  # Move forward at 50% speed
    time.sleep(2)

    print("Motors moving backward")
    set_motor(50, "backward")  # Move backward at 50% speed
    time.sleep(2)

    print("Stopping motors")
    set_motor(0, "stop")  # Stop all motors

except KeyboardInterrupt:
    print("Stopping motors and cleaning up")
    set_motor(0, "stop")
    GPIO.cleanup()
