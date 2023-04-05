#include <Arduino.h>
#include <FastLED.h>
#include <string.h>

#define SERIAL_BYTE	6

#define LED_PIN	2
#define LED_NUM	12

unsigned long mill = 0;
char serial_bytes[SERIAL_BYTE] = {};
bool set_led = false;

CRGB leds[LED_NUM];

void setup()
{
	FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, LED_NUM);
	FastLED.clearData();
	FastLED.show();

	Serial.begin(115200);
	Serial.setTimeout(100);							// 100ms
}

bool ReadSerial()
{
	unsigned long cmill = millis();
	
	if (cmill - mill > 10)
	{
		mill = cmill;
		// read serial bytes
		if (Serial.readBytes(serial_bytes, SERIAL_BYTE) == SERIAL_BYTE)
		{
			if (serial_bytes[5] == 0x79)
			{
				Serial.flush();

				return true;
			}
		}
	}

	return false;
}

void SetupLED()
{
	if(serial_bytes[0] == 0x01 && serial_bytes[5] == 0x79)			// Turn On
	{
		if (serial_bytes[1] == 0x00)			// R
		{
			for(int i = 0; i < LED_NUM; i++)
				leds[i] = CRGB(255, 0, 0);
			FastLED.show();
		}
		else if (serial_bytes[1] == 0x01)		// G
		{
			for(int i = 0; i < LED_NUM; i++)
				leds[i] = CRGB(0, 255, 0);
			FastLED.show();
		}
		else if (serial_bytes[1] == 0x02)		// B
		{
			for(int i = 0; i < LED_NUM; i++)
				leds[i] = CRGB(0, 0, 255);
			FastLED.show();
		}
		else if (serial_bytes[1] == 0x03)		// Custom
		{
			for(int i = 0; i < LED_NUM; i++)
				leds[i] = CRGB(serial_bytes[2], serial_bytes[3], serial_bytes[4]);
			FastLED.show();			
		}

	}
	else if (serial_bytes[0] == 0x00 && serial_bytes[5] == 0x79)	// Turn Off
	{
		FastLED.clearData();
		FastLED.show();
	}
}

void loop()
{
	set_led = ReadSerial();

	if(set_led)
	{
		SetupLED();
	}
}
