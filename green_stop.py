import cv2
import numpy as np
import pyfirmata

# Define board and pins connected to the stepper motor
board = pyfirmata.Arduino('/dev/ttyACM0')
motor_pins = [8, 9, 10, 11]
delay_time = 0.005
steps_per_revolution = 200
motor_speed = 60

# Initialize the stepper motor
motor = pyfirmata.util.StepperMotor(board, motor_pins[0], motor_pins[1], motor_pins[2], motor_pins[3], steps_per_revolution)

# Start the board
board.digital[13].write(1)
board.iterate()

# Rotate the stepper motor one full revolution clockwise
motor.setSpeed(motor_speed)
motor.step(steps_per_revolution)

# Wait for 1 second
time.sleep(1)

# Rotate the stepper motor one full revolution counterclockwise
motor.setSpeed(motor_speed)
motor.step(-steps_per_revolution)

# Wait for 1 second
time.sleep(1)

# Stop the board
board.digital[13].write(0)
board.iterate()

for pin in motorPins:
    board.digital[pin].mode = pyfirmata.OUTPUT

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # lower and upper bounds for red color
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask_red1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red2 = np.array([170,50,50])
    upper_red2 = np.array([180,255,255])
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # lower and upper bounds for green color
    lower_green = np.array([36, 25, 25])
    upper_green = np.array([70, 255,255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # lower and upper bounds for blue color
    lower_blue = np.array([50, 50, 0])
    upper_blue = np.array([255,255,180])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Mergers all maska together into one mask  
    mask = cv2.bitwise_or(mask_blue, cv2.bitwise_or(mask_green, mask_red))
    # contours are the shapes that the camera recognises as one object on screen, 
    # it uses the mask variable as what colors it needs to detect
    # cv2.RETR_TREE : retrevial in tree mode, retrieves all objects(smarties) and organises them into a heiharchy , parent child relationship
    smarties, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for smartie in smarties:
        area = cv2.contourArea(smartie)
        if area > 9000:
            x, y, w, h = cv2.boundingRect(smartie)
            color = (0, 0, 0)
            if mask_red[y:y+h, x:x+w].any():
                color = (0, 0, 255) # red color
                cv2.putText(frame, "Red Smartie", (x, y), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
            elif mask_green[y:y+h, x:x+w].any():
                color = (0, 255, 0) # green color
                cv2.putText(frame, "Green Smartie", (x, y), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
                # Stop the stepper motor
                for pin in motorPins:
                    board.digital[pin].write(0)
                break
            elif mask_blue[y:y+h, x:x+w].any():
                color = (255, 0, 0) # blue color
                cv2.putText(frame, "Blue Smartie", (x, y), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
