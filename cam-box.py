import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #lower red	
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    #upper red
    lower_red2 = np.array([170,50,50])
    upper_red2 = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = cv2.bitwise_or(mask1, mask2)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Red Smartie", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            is_red = True
        else:
            is_red = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    cv2.imshow("Frame", frame)

cap.release()
cv2.destroyAllWindows()
