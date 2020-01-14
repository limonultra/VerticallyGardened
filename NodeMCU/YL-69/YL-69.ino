void setup() {
  pinMode(D6, INPUT); /* Pin por el que vamos a recibir la humedad */
  Serial.begin(9600); /* Para imprimir por pantalla usando puerto serial */
}

void loop() {
  int hum = digitalRead(D6);
  Serial.println(hum);

  delay(500);
}
