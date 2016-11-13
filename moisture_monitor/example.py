# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time
import requests

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
CLK  = 22 
MISO = 27 
MOSI = 17 
CS   = 4  
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)

output = ""
# Main program loop.
values = []
for x in range(0,10):    
  # Read all the ADC channel values in a list.
    read = mcp.read_adc(0)
    # Print the ADC values.
    values[x] = foo 
    time.sleep(0.5)

url = 'http://www.pleasetakecareofmyplant.com/datatest.php'
payload = {'foo':values}
r = requests.post(url, data=payload)
