#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "Holberton - Students";
const char* password = "HBTNStuds24";

int relayPinWater = 3;
int relayPinLight = 2;

bool switchStateWater = false;
bool switchStateLight = false;

WiFiClient wifiClient;

void setup() {
  pinMode(relayPinWater, OUTPUT);
  pinMode(relayPinLight, OUTPUT);

  digitalWrite(relayPinWater, LOW);
  digitalWrite(relayPinLight, LOW);

  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
  }

  Serial.println("Connected to WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED)
  {

    checkState("172.17.221.251:5000/waterstate", relayPinWater, switchStateWater);


    checkState("172.17.221.251:5000/lightstate", relayPinLight, switchStateLight);
  }
  else
  {
    Serial.println("WiFi not connected");
  }

  delay(5000);
}

void checkState(const char* url, int relayPin, bool& switchState) {
  HTTPClient http;
  http.begin(wifiClient, url);
  int httpCode = http.GET();

  if (httpCode > 0)
  {
    String payload = http.getString();
    Serial.print("Payload from ");
    Serial.println(url);
    Serial.println(payload);

    if (payload.indexOf("on") > -1)
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
      Serial.println("Switching ON relay");
    }
    else
    {
      digitalWrite(relayPin, LOW);
      Serial.println("Switching OFF relay");
    }
  }
  else
  {
    Serial.println("Error on HTTP request");
  }

  http.end();
}