import serial
import time
import string
import pynmea2

import digitalio
import board

from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors
from PIL import Image, ImageDraw, ImageFont
from time import strftime, sleep
import geopy.distance

# The display uses a communication protocol called SPI.
# SPI will not be covered in depth in this course. 
# you can read more https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # the rate  the screen talks to the pi
# Setup SPI bus using hardware SPI:
spi = board.SPI()
# Create the ST7789 display:
disp = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)


# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
font16 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
font20 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)


# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

draw.rectangle((0, 0, width, height), outline=0, fill=0)
draw.text((x, 10),"<--- Start Run" , font=font20, fill="#4DFF19")
disp.image(image, rotation)
startRun = False
startLat = 0.0
startLon = 0.0
totDist = 0.0
totTime = 0.0


while True:

    port = "/dev/ttyACM0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline()

    if newdata[0:6] == b'$GPRMC':
        
        newmsg=pynmea2.parse(newdata.decode())
        lat=newmsg.latitude
        lng=newmsg.longitude
        gps = "Latitude: " + str(lat) + "and Longitude: " + str(lng)

        strLat = "Latitude: " + str(lat)
        strLong = "Longitude: " + str(lng)


        if buttonB.value and not buttonA.value:  # just button A pressed
            
            startRun = True
            startLat = lat
            startLon = lng
            totDist = 0.0
            totTime = 0.0
        
        if buttonA.value and not buttonB.value:
            
            startRun = False
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            y = top
            draw.text((x, top + 10),"Run Ended" , font=font20, fill="#4DFF19")
            y += font16.getsize("Run Ended")[1]
            draw.text((x, y + 15), "Final Distance: "+str(totDist), font=font16, fill="#FFFFFF")
            y += font16.getsize("Final Distance: " + str(totDist) + " miles")[1]
            draw.text((x, y + 20), "Total Time: " + str(totTime) + "s", font=font16, fill="#FFFFFF")
            y += font16.getsize("Total Time: " + str(totDist))[1]
            draw.text((x, y + 25), "Avg Speed: " + str(totDist*3600/totTime) + " mi/hr", font=font16, fill="#FFFFFF")
            disp.image(image, rotation)

            time.sleep(5)

            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((x, 10),"<--- Start Run" , font=font20, fill="#4DFF19")
            disp.image(image, rotation)
            startRun = False
            startLat = 0.0
            startLon = 0.0
            totDist = 0.0
            totTime = 0.0

        if startRun:
            
            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, width, height), outline=0, fill=0)

            y = top
            metricsmsg = "Metrics"
            draw.text((x, y), "Metrics", font=font20, fill="#C89CFF")

            #Print Latitude and Longtitude Values
            y += font20.getsize(metricsmsg)[1]
            draw.text((x, y), strLat, font=font16, fill="#FFFFFF")
            y += font16.getsize(strLat)[1]
            draw.text((x, y), strLong, font=font16, fill="#FFFFFF")

            # Display Distance.
            coords_1 = (startLat, startLon)
            coords_2 = (lat, lng)

            distance = geopy.distance.distance(coords_1, coords_2).miles
            totDist += distance

            y += font16.getsize(strLong)[1]
            draw.text((x, y), "Distance: " + str(totDist) + " miles", font=font16, fill="#FFFFFF")

            # Display Time
            y += font16.getsize("Distance: " + str(totDist))[1]
            draw.text((x, y), "Time: "+str(totTime), font=font16, fill="#FFFFFF")

            draw.text((x, height - 30), "Time: "+str(totTime), font=font16, fill="#FFFFFF")

            disp.image(image, rotation)
            time.sleep(0.5)
            totTime+=0.5
        
        print(gps)

