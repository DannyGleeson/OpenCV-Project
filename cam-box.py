import cv2
import numpy as np

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
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    mask = cv2.bitwise_or(mask_red, cv2.bitwise_or(mask_green, mask_blue))
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10000:
            x, y, w, h = cv2.boundingRect(contour)
            color = (0, 0, 0)
            if mask_red[y:y+h, x:x+w].any():
                color = (0, 0, 255) # red color
                cv2.putText(frame, "Red Smartie", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            elif mask_green[y:y+h, x:x+w].any():
                color = (0, 255, 0) # green color
                cv2.putText(frame, "Green Smartie", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            elif mask_blue[y:y+h, x:x+w].any():
                color = (255, 0, 0) # blue color
                cv2.putText(frame, "Blue Smartie", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
