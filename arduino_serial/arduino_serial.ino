

char data[10];

void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);
  
}

// the loop routine runs over and over again forever:
void loop() {
  //Serial.write(1234);
  Serial.print(1234);
  delay(100);
 

    if (Serial.available() >= 0)
{
  Serial.readBytesUntil('\x04',data,10);
  delay(100);
}

Serial.println(data);
delay(100);
memset(data, 0, sizeof(data));
Serial.flush();
delay(10);
  
}
