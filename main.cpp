#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>

const char* ssid = "Holberton - Students";
const char* password = "HBTNStuds24";

int PinWater = 5;
int PinLight = 2;
bool switchStateWater = false;
bool switchStateLight = false;

WiFiClientSecure wifiClientSecure;

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
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");

  wifiClientSecure.setInsecure();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED)
  {
    checkState("https://smart-office.onrender.com/waterstate/1", relayPinWater, switchStateWater);
    checkState("https://smart-office.onrender.com/lightstate/1", relayPinLight, switchStateLight);
  }
  else
  {
    Serial.println("WiFi not connected");
  }

  delay(1000);
}

void checkState(const char* url, int relayPin, bool& switchState) {
  HTTPClient http;
  http.begin(wifiClientSecure, url);
  int httpCode = http.GET();

  if (httpCode == HTTP_CODE_MOVED_PERMANENTLY || httpCode == HTTP_CODE_FOUND) {
    String newUrl = http.getLocation();
    Serial.print("Redirected to: ");
    Serial.println(newUrl);

    http.end();

    http.begin(wifiClientSecure, newUrl);
    httpCode = http.GET();
  }

  if (httpCode > 0)
  {
    String payload = http.getString();
    Serial.print("Payload from ");
    Serial.println(url);
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