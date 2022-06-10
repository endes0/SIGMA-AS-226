# SIGMA AS 226
## Hardware
![](HW%20photos/main_board_top.jpg)
### Microcontroller
[Mitsubishi M5l8048](https://happytrees.org/files/chips/datasheets/datasheet-Mitsubishi--M5L8049--M5L8039.pdf)
* [Reference manual](http://www.bitsavers.org/components/mitsubishi/_dataBooks/1986_Mitsubishi_Single_Chip_8-Bit_Vol2.pdf)
* MELPS 8-48 architecture
* 6 MHz
* Internal ROM
* 128 Bytes RAM
* 2 KB ROM (?)
### External RAM
[HM6264LP-70](https://www.alldatasheet.com/datasheet-pdf/pdf/64396/hitachi/hm6264lp-70.html)
* 8192 Bytes
* Connected to the battery
* It keeps the programmed text
* Connected to the EPROM, maybe the EPROM reloads the default data to the RAM if the battery is low?
### EPROM
[Intel D27128](https://archive.org/details/IntelD27128Datasheet)
* 128 Kb
* Dumped the content on `/Eprom dump`
* [Dumping tutorial](https://danceswithferrets.org/geekblog/?p=315)
* Fixed dumper code on `/Intel-Eprom-code`
### Clock Ic (?)
ASLC AX5210B
* did not find any info about this
* connected to the battery
* maybe is the IC for the real time clock functionality?

## RS232
[a pretty good documentation(it is in german)](http://sigma.haufe.org/index.php?content=home).
Only the RX line is really connected to the microcontroller. Also, the microcontroller does not have a serial port, so it is implemented virtually, using the interupt pin. 

## Python scripts
### enconde_and_send.py
It will program the content of `text.txt` to the display.
### tg_bot.py
A small Telegram bot that will send the messages replayed with the `/display` command or a formated text with `/gen`