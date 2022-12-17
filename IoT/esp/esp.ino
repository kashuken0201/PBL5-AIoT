#include <WebServer.h>
#include <C:\Users\chiho\AppData\Local\Arduino15\packages\esp32\hardware\esp32\2.0.3-RC1\libraries\WiFi\src\WiFi.h>
#include <esp32cam.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>

#define LCD_SDA 13
#define LCD_SCL 15
#define SOUND_PIN 14

LiquidCrystal_I2C lcd(0x27, 16, 2); // 14 15
WebServer server(80);

const char *WIFI_SSID = "Kashuken";
const char *WIFI_PASS = "0702580427";
// const char *WIFI_SSID = "phat";
// const char *WIFI_PASS = "12345678";
// const char *WIFI_SSID = "Khu C";
// const char *WIFI_PASS = "khu@c2022";

const char *host = "192.168.1.18";
const int port = 8888;

WiFiClient client;

// static auto loRes = esp32cam::Resolution::find(320, 240);
// static auto midRes = esp32cam::Resolution::find(350, 530);
static auto hiRes = esp32cam::Resolution::find(416, 416);
void serveJpg()
{
    auto frame = esp32cam::capture();
    if (frame == nullptr)
    {
        Serial.println("CAPTURE FAIL");
        server.send(503, "", "");
        return;
    }

    server.setContentLength(frame->size());
    server.send(200, "image/jpeg");
    WiFiClient client = server.client();
    frame->writeTo(client);
}

void setup()
{
    pinMode(SOUND_PIN, OUTPUT);
    Serial.begin(115200);
    Serial.println();

    // initialize the LCD,
    Wire.begin(LCD_SDA, LCD_SCL);
    lcd.init();
    lcd.backlight();
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Hello");

    // initialize the camera
    {
        using namespace esp32cam;
        Config cfg;
        cfg.setPins(pins::AiThinker);
        cfg.setResolution(hiRes);
        cfg.setBufferCount(2);
        cfg.setJpeg(80);

        bool ok = Camera.begin(cfg);
        Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
    }

    // initialize the WiFi
    WiFi.persistent(false);
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("Connection to wifi failed");
        delay(500);
    }

    // receive IP address
    Serial.println("Connected to WiFi");
    Serial.print("http://");
    Serial.print(WiFi.localIP());
    Serial.println("/cam.jpg");

    // initialize the server
    server.on("/cam.jpg", serveJpg);
    server.begin();

    while (!client.connect(host, port))
    {
        Serial.println("Connection to server failed");
        delay(1000);
    }
    Serial.println("Connection to server successfully");
}

void loop()
{
    server.handleClient();
    String msg = "";

    if (WiFi.status() == WL_CONNECTED && client.connected())
    {
        while (client.available())
        {
            char c = client.read();
            if (c == '\n')
            {
                Serial.println(msg);
                if (msg.equals(""))
                {
                    lcd.clear();
                    digitalWrite(SOUND_PIN, LOW);
                }
                else
                {
                    lcd.clear();
                    lcd.setCursor(0, 0);
                    lcd.print("Ban " + msg);
                    lcd.setCursor(0, 1);
                    lcd.print("vui long deo khau trang");
                    digitalWrite(SOUND_PIN, HIGH);
                }
                break;
            }
            else
            {
                msg += c;
            }
        }
    }
    // if the server's disconnected, stop the client:
    else
    {
        Serial.println("Disconnected to wifi");
        while (WiFi.status() != WL_CONNECTED)
        {
            Serial.println("Connection to wifi failed");
            delay(500);
        }
        Serial.println("Connected to wifi");
        if (!client.connected())
        {
            Serial.println("Connection to server failed");
            delay(1000);
            while (!client.connect(host, port))
            {
                Serial.println("Connection to server failed");
                delay(1000);
            }
            Serial.println("Connection to server successfully");
        }
    }
}
