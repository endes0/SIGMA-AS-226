#include <Arduino.h>

/*
ROM Reader. Quick Arduino program to read a parallel-accessed ROM and dump it to the serial
port in hex.

Oddbloke. 16th Feb 2014.
 */
 
// How I've wired the digital pins on my Arduino to the address and data pins on
// the ROM.
static const int kPin_A0  = 38;
static const int kPin_A1  = 36;
static const int kPin_A2  = 34;
static const int kPin_A3  = 32;
static const int kPin_A4  = 30;
static const int kPin_A5  = 28;
static const int kPin_A6  = 26;
static const int kPin_A7  = 24;
static const int kPin_A8  = 33;
static const int kPin_A9  = 35;
static const int kPin_A10 = 39;
static const int kPin_A11 = 37;
static const int kPin_A12 = 22;
static const int kPin_A13 = 31;

static const int kPin_D0 = 40;
static const int kPin_D1 = 42;
static const int kPin_D2 = 44;
static const int kPin_D3 = 49;
static const int kPin_D4 = 47;
static const int kPin_D5 = 45;
static const int kPin_D6 = 43;
static const int kPin_D7 = 41;

void setup()
{
  // set the address lines as outputs ...
  pinMode(kPin_A0, OUTPUT);     
  pinMode(kPin_A1, OUTPUT);     
  pinMode(kPin_A2, OUTPUT);     
  pinMode(kPin_A3, OUTPUT);     
  pinMode(kPin_A4, OUTPUT);     
  pinMode(kPin_A5, OUTPUT);     
  pinMode(kPin_A6, OUTPUT);     
  pinMode(kPin_A7, OUTPUT);     
  pinMode(kPin_A8, OUTPUT);     
  pinMode(kPin_A9, OUTPUT);     
  pinMode(kPin_A10, OUTPUT);     
  pinMode(kPin_A11, OUTPUT);     
  pinMode(kPin_A12, OUTPUT);     
  pinMode(kPin_A13, OUTPUT);
 
  // set the data lines as inputs ...
  pinMode(kPin_D0, INPUT); 
  pinMode(kPin_D1, INPUT); 
  pinMode(kPin_D2, INPUT); 
  pinMode(kPin_D3, INPUT); 
  pinMode(kPin_D4, INPUT); 
  pinMode(kPin_D5, INPUT); 
  pinMode(kPin_D6, INPUT); 
  pinMode(kPin_D7, INPUT); 
  
  Serial.begin(9600);
}

void SetAddress(int addr)
{
  // update the address lines to reflect the address we want ...
  digitalWrite(kPin_A0, (addr & 1)?HIGH:LOW);
  digitalWrite(kPin_A1, (addr & 2)?HIGH:LOW);
  digitalWrite(kPin_A2, (addr & 4)?HIGH:LOW);
  digitalWrite(kPin_A3, (addr & 8)?HIGH:LOW);
  digitalWrite(kPin_A4, (addr & 16)?HIGH:LOW);
  digitalWrite(kPin_A5, (addr & 32)?HIGH:LOW);
  digitalWrite(kPin_A6, (addr & 64)?HIGH:LOW);
  digitalWrite(kPin_A7, (addr & 128)?HIGH:LOW);
  digitalWrite(kPin_A8, (addr & 256)?HIGH:LOW);
  digitalWrite(kPin_A9, (addr & 512)?HIGH:LOW);
  digitalWrite(kPin_A10, (addr & 1024)?HIGH:LOW);
  digitalWrite(kPin_A11, (addr & 2048)?HIGH:LOW);
  digitalWrite(kPin_A12, (addr & 4096)?HIGH:LOW);
  digitalWrite(kPin_A13, (addr & 8192)?HIGH:LOW);
}

byte ReadByte()
{
  // read the current eight-bit byte being output by the ROM ...
  byte b = 0;
  if (digitalRead(kPin_D0)) b |= 1;
  if (digitalRead(kPin_D1)) b |= 2;
  if (digitalRead(kPin_D2)) b |= 4;
  if (digitalRead(kPin_D3)) b |= 8;
  if (digitalRead(kPin_D4)) b |= 16;
  if (digitalRead(kPin_D5)) b |= 32;
  if (digitalRead(kPin_D6)) b |= 64;
  if (digitalRead(kPin_D7)) b |= 128;
  
  return(b);
}

void loop()
{
  int addr;
  
  // The only reason I'm choosing to read in blocks of 16 bytes
  // is to keep the hex-dump code simple. You could just as easily
  // read a single byte at a time if that's all you needed.
  
  Serial.println("Reading ROM ...\n");
  delay(1000);

  for (addr = 0; addr < 16384 * 16; addr += 1)
  {
      SetAddress(addr); // tells the ROM the byte we want ...
      delay(5);
      Serial.write(ReadByte());
  }
  
  // All done, so lockup ...
  while (true) {delay(10000);}
}
