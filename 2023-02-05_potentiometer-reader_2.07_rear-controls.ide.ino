// Set the pin for the toggle switch
int button = 8;

void setup() {
  // set up the serial connection
  Serial.begin(9600);
  
  // set the pin modes for the potentiometers
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);

  // set the toggle switch
  pinMode(button,INPUT_PULLUP); // Unpressed button is high
}

void loop() {
  if (Serial.available() > 0) {
    // read the incoming command
    char command = Serial.read();
    
    if (command == 'r') {
      if(digitalRead(button) == true) {
        // read the values from the potentiometers using the front values.
        int val1 = analogRead(A0);
        int val2 = analogRead(A1);
        int val3 = analogRead(A2);
        
        // send the values back to the Linux computer
        Serial.print(val1);
        Serial.print(",");
        Serial.print(val2);
        Serial.print(",");
        Serial.println(val3);
      }
      if(digitalRead(button) == false) {
        // read the values from the potentiometers using the rear values.
        int val1 = analogRead(A3);
        int val2 = analogRead(A4);
        int val3 = analogRead(A5);
        
        // send the values back to the Linux computer
        Serial.print(val1);
        Serial.print(",");
        Serial.print(val2);
        Serial.print(",");
        Serial.println(val3);
      }
    }
  }
}
