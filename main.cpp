#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "Holberton - Students";
const char* password = "HBTNStuds24";

int relayPin = 7;
bool switchState = false;

void setup() {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);
  
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED)
  {
    HTTPClient http;
    http.begin("172.17.208.1");
    int httpCode = http.GET();

    if (httpCode > 0)
    {
      String payload = http.getString();
      Serial.println(payload);

      if (payload.indexOf("true") > -1)
      {
        switchState = true;
      }
      else
      {
        switchState = false;
      }

      if (switchState)
      {
        digitalWrite(relayPin, HIGH);
      }
      else
      {
        digitalWrite(relayPin, LOW);
      }
    } 
    else
    {
      Serial.println("Error on HTTP request");
    }

    http.end();
  }

  delay(5000);
}
