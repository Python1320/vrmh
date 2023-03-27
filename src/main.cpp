
#include <ArduinoOSCWiFi.h>

const char* ssid = "ssid";
const char* pwd = "";

const IPAddress ip(10, 0, 0, 123);
const IPAddress gateway(10, 0, 0, 1);
const IPAddress subnet(255, 0,0 , 0);

// 12 = wemos  D6
const uint8_t OUT = 12;

const int recv_port = 54321;


int i;
float f;
String s;


void setBrr(int brr)  { 
#ifdef CANSER
  Serial.print("Brr=");
  Serial.print(brr);
  Serial.println();
#endif
  if (brr==0) {
	digitalWrite(OUT, 0);
} else if (brr>255) {
	digitalWrite(OUT, 1);
} else {
	analogWrite(OUT, brr);
}
}

void setup() {

  pinMode(OUT, OUTPUT);
  analogWriteFreq(300);
#ifdef CANSER
    Serial.begin(9600);
    delay(2000);
#endif

#ifdef ESP_PLATFORM
    WiFi.disconnect(true, true);
    delay(1000);
    WiFi.mode(WIFI_STA);
#endif
    WiFi.begin(ssid, pwd);
    WiFi.config(ip, gateway, subnet);
    while (WiFi.status() != WL_CONNECTED) {
#ifdef CANSER
        Serial.print(".");
#endif
        delay(500);
    }
#ifdef CANSER
    Serial.print("WiFi connected, IP = ");
    Serial.println(WiFi.localIP());
#endif
    OscWiFi.subscribe(recv_port, "/brr",
        [](const OscMessage& m) {
#ifdef CANSER
            Serial.print(m.remoteIP());
            Serial.print(" ");
            Serial.print(m.remotePort());
            Serial.print(" ");
            Serial.print(m.size());
            Serial.print(" ");
            Serial.print(m.address());
            Serial.print(" ");
            Serial.print(m.arg<float>(0));

            Serial.println(".");
#endif
            setBrr((int)(255.0f*m.arg<float>(0)));
        });


}

void loop() {
    OscWiFi.update();
    analogWriteFreq(random(200,500));
}
