
#include <Stepper.h>

// Define the number of steps per revolution
const int stepsPerRevolution = 200;

// Initialize the stepper motor with the number of steps and the pins connected to the motor
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {       
  // Set the speed of the stepper motor (in RPM)
  myStepper.setSpeed(60);
}

void loop() {
  // Rotate the stepper motor one full revolution clockwise
  myStepper.step(stepsPerRevolution);
  delay(1000); // Wait for 1 second

  // Rotate the stepper motor one full revolution counterclockwise
  myStepper.step(-stepsPerRevolution);
  delay(1000); // Wait for 1 second
}
