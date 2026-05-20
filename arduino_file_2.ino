int rPin = 3;
int gPin = 5;
int bPin = 6;
int ambientPin = 9;

String data = "";

void setup() {
  Serial.begin(9600);

  pinMode(rPin, OUTPUT);
  pinMode(gPin, OUTPUT);
  pinMode(bPin, OUTPUT);
  pinMode(ambientPin, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    data = Serial.readStringUntil('\n');

    int r, g, b, ambient;

    sscanf(data.c_str(), "%d,%d,%d,%d", &r, &g, &b, &ambient);

    analogWrite(rPin, r);
    analogWrite(gPin, g);
    analogWrite(bPin, b);
    analogWrite(ambientPin, ambient);
  }
}