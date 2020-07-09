SRC=blink
BOARD=atmega2560
DUDEBOARD=m2560
PORT=/dev/ttyACM0 

CC=avr-g++
ARDUINOBASE=/usr/share/arduino/hardware
ARDUINOTOOLS=$(ARDUINOBASE)/tools
ARDUINO=$(ARDUINOBASE)/arduino
LIBPATH=$(ARDUINO)/cores/arduino
LIBS=$(LIBPATH)/HardwareSerial.cpp $(LIBPATH)/wiring_digital.c $(LIBPATH)/wiring_shift.c $(LIBPATH)/wiring.c $(LIBPATH)/Print.cpp $(LIBPATH)/WString.cpp $(LIBPATH)/new.cpp

OBJECTS=HardwareSerial.o wiring_digital.o wiring_shift.o wiring.o Print.o WString.o new.o

CPPFLAGS=-DF_CPU=16000000 -mmcu=$(BOARD) -I$(ARDUINO)/variants/mega -I$(LIBPATH)


compile:	$(OBJECTS)
	$(CC) -Os $(CPPFLAGS) $(SRC).c $(OBJECTS) -o $(SRC).elf
	avr-objcopy -O ihex -R .eeprom $(SRC).elf $(SRC).ihex	

$(OBJECTS):
	$(CC) -c $(CPPFLAGS) $(LIBS)

upload:
	avrdude -v -C $(ARDUINOTOOLS)/avrdude.conf -b 115200 -c avrisp2 -p $(DUDEBOARD) -P $(PORT) -U flash:w:$(SRC).ihex:i 


clean:
	rm $(OBJECTS) $(SRC).elf $(SRC).ihex
