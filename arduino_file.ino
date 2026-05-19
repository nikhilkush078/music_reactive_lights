// PWM pins
const int RED_PIN = 3;
const int GREEN_PIN = 5;
const int BLUE_PIN = 6;

String inputString = "";
bool stringComplete = false;

void setup() {
  Serial.begin(115200);

  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
}

void loop() {
  if (stringComplete) {
    int r, g, b;

    // Parse "R,G,B"
    sscanf(inputString.c_str(), "%d,%d,%d", &r, &g, &b);

    // Apply PWM
    analogWrite(RED_PIN, r);
    analogWrite(GREEN_PIN, g);
    analogWrite(BLUE_PIN, b);

    inputString = "";
    stringComplete = false;
  }
}

// Serial event
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;

    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}