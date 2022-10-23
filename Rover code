#include <ArduinoMotorCarrier.h>
int throttleVal;
int throttlepin = A2;
int servVal;
int servPin = A7;
int dutee = 0;
int steerAngle;
void setup()
{
// Setup section was copy and pasted from "Examples" section of motorcarrier library - not my code

  //Serial port initialization
  Serial.begin(115200);
  //while (!Serial);

  //Establishing the communication with the Motor Carrier
  if (controller.begin())
  {
    Serial.print("Motor Carrier connected, firmware version ");
    Serial.println(controller.getFWVersion());
  }
  else
  {
    Serial.println("Couldn't connect! Is the red LED blinking? You may need to update the firmware with FWUpdater sketch");
    while (1);
  }

  // Reboot the motor controller; brings every value back to default
  Serial.println("reboot");
  controller.reboot();
  delay(500);

}

void loop() {

throttleVal = analogRead(throttlepin);
Serial.println(throttleVal);

if (throttleVal < 450){
  dutee = map(throttleVal, 0, 450, -100, 0);
}
else if (throttleVal > 550){
  dutee = map(throttleVal, 550, 1024, 0, 100);
}
else{
  dutee = 0;
}

servVal = analogRead(servPin);
if (servVal < 450){
  steerAngle = map(servVal, 0, 450, 60, 90);
}
else if (servVal > 550){
  steerAngle = map(servVal, 550, 1045, 90, 120);
}
else{
  steerAngle = 90;
}
M2.setDuty(dutee);
M1.setDuty(dutee*(-1));
servo1.setAngle(steerAngle);
delay(50);
}
