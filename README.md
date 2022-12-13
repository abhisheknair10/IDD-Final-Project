# IDD-Final-Project Documentation

Collaborators:

1. Abhishek Nair - an464@cornell.edu
2. Vikram Pandian - vip6@cornell.edu

This is the [Developing and Designing Interactive Devices](https://www.tech.cornell.edu/news/courses/developing-and-designing-interactive-devices-2/) Final Project as part of the Cornell Tech Master of Engineering Program.

# Introduction

The Internet of Things and Interactive Devices is the field of technology that deals with physical objects with computational capabilties, sensors and actuators that can connect to any form of network, including the internet, to exchange data with other devices, servers or the cloud.

This project aims to make use of this concept to build a GPS tracker based system for running enthusiasts to track their runs and workouts. A runner will be able to take the device with them while on a run. During this time, the Raspberry Pi will stream the GPS data as well as time data to a remote server via WiFi or Cellular. The server will then store this data and allow the user to view it on a web interface. The user will be able to view the route they took on a map, as well as the time it took them to complete the run. The user will also be able to view their average speed, distance, and other statistics. The user will also be able to view their previous runs and compare them to each other.

The aim of this assignment is to:

1. Build and connect the hardware components
2. Receive and process GPS data from the GPS module
3. Send GPS data to a remote server
4. Serve the data on a web dashboard

## Timeline

<p align="center">
  <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/Project%20Timeline.png" width="800" title="IDD Slide">
</p>

1. 17 November - Order parts
2. 25 November - Receive parts
3. 25 November - Start building prototype
4. 29 November - Finish first draft of prototype for testing, validation and for functional check off
5. 30 November - Take feedback from course instructors and make changes to prototype
6. 3 December - Finish final working prototype ready for submission
7. 4 December - Build dashboard and website for runners to view their workouts
8. 5 December - Complete documentation and submit project


[Here](https://github.com/abhisheknair10/IDD-Final-Project/blob/main/ProjectPlan.md) is the preliminary project plan

# Table of Contents

<div align="center">

| No      |  Title 
| :---:   | :---: 
| 1.      | [About the Hardware](https://github.com/abhisheknair10/IDD-Final-Project#1-about-the-hardware)
| 2.      | [The Run Tracking Software on the Raspberry Pi](https://github.com/abhisheknair10/IDD-Final-Project#2-the-run-tracking-software-on-the-raspberry-pi)
| 3.      | [Building the User Interface for the System](https://github.com/abhisheknair10/IDD-Final-Project#3-building-the-user-interface-for-the-system)
| 4.      | [Cloud Server Development](https://github.com/abhisheknair10/IDD-Final-Project#4-cloud-server-development)
| 5.      | [Client Side Development](https://github.com/abhisheknair10/IDD-Final-Project#5-client-side-development)
| 6.      | [Testing Results and Conclusions](https://github.com/abhisheknair10/IDD-Final-Project#6-testing-results-and-conclusions)

</div>

To understand how the different parts of this project and different services communicate with each other to create a valuable application, below is a diagram of the app architecture.

<p align="center">
    <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/architecture.png" width="600" title="IDD Slide">
</p>

A storyboard of the events and interaction between the the different parts of the system and the user is shown below.

<p align="center">
    <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/storyboard.png" width="600" title="IDD Slide">
</p>

# 1. About the Hardware

## 1.1. Raspberry Pi 3 B+

The Raspberry Pi 3 B+ is a ARMv8 64bit based processor that can run a Linux based operating system. It has 1GB of RAM and 4 USB ports. It also has a 40 pin GPIO header that can be used to connect external hardware to the Raspberry Pi. The Raspberry Pi 3 B+ is a very popular single board computer that is used in many projects due to its low cost and high performance.

For this application, the Debian based Raspbian OS is used which is Linux based OS that is specifically designed for the Raspberry Pi.

<p align="center">
    <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/raspberrypi.png" width="300" title="Neo 6M">
</p>

## 1.2. Neo 6M GPS Module

The Neo 6M GPS module is a GPS module that can be connected to the Raspberry Pi via the USB port for newer versions. It has a connected antenna that can be used to receive GPS signals from up to 22 satellites across 50 channels. 

<p align="center">
    <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/neo6m.png" width="300" title="Neo 6M">
</p>

Interfacing the Neo 6M with the Raspberry Pi requires running some UNIX commands in the command line. The commands are as follows:

1. Install gpsd:
    ```bash
    sudo apt-get install gpsd gpsd-clients
    ```

2. Identify all the ports on the Raspberry Pi and find the tty identifier that is associated with the GPS module:
    ```bash
    ```bash
    ls -l /dev/tty*
    ```
For our specific device, the port was /dev/ttyAMA0.

This port needs to be noted down when running the python file to read the GPS data from the correct port at a baud rate of 9600.

# 2. The Run Tracking Software on the Raspberry Pi

The Neo 6M GPS module is based on the principle of triangulation. It receives signals from up to 22 satellites across 50 channels. The GPS module then uses the time difference of arrival of the signals from the satellites to calculate the distance between the GPS module and the satellites. This varying distance from multiple sources is then used to calculate the accurate latitude and longitude of the GPS module which is then streamed to the Raspberry Pi.

Since we are using a versatile and open language such as Python, community developed libraries can be used to make interfacing with the GPS module relatively straightforward. The [pynmea2](https://github.com/Knio/pynmea2) module is a Python module based on the NMEA 0183 protocol which is a protocol and data specification for communication between marine electronics such as echo sounder, sonars, anemometer, gyrocompass, autopilot, GPS receivers and many other types of instruments.

The pynmea2 module can be used to parse the NMEA data that is received from the GPS module and extract the latitude and longitude data. This is done by:

1. Importing the pynmea2 module:
    ```python
    import pynmea2
    ```

2. Opening the serial port that is connected to the GPS module:
    ```python
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    ```

3. Reading the data from the serial port:
    ```python
    data = ser.readline()
    ```

4. Parsing the data using the pynmea2 module:
    ```python
    if data[0:6] == b'$GPRMC':
        msg = pynmea2.parse(data)
        lat = round(msg.latitude, 6)
        lon = round(msg.longitude, 6)
    ```

Hence, using the above steps, we can find the GPS coordinates of the module accurate to 2.5 metres. Functions and code for the specific application is pretty straightforward to build for an experienced software engineer and programmer and hence, is covered in [main.py](https://github.com/abhisheknair10/IDD-Final-Project/blob/main/raspberrypi/main.py).

For steps on how to setup the display to display the appropriate messages at the appropriate times, the [adafruit_rgb_display](https://docs.circuitpython.org/projects/rgb_display/en/latest/api.html#adafruit-rgb-display-st7789) module was used. Displaying a message is done using the following code:

```python
draw.rectangle((0, 0, width, height), outline=0, fill=0)
y = top
draw.text(
    (x, y),
    "Display Message", 
    font=font20,
    fill="#4DFF19"
)
y += font16.getsize("Run Ended")[1]
disp.image(image, rotation)
```

Some initial software setting up is required before the above code can run which is shown below:

```python
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
```

This sets up the buttons and the backlight and tells the Raspberry Pi to treat the GPIO pins as digitalIO vs analogIO. The backlight is set to True to turn on the backlight of the display.

The original source of the code to setup the display is available and the [Cornell Tech Interactive Lab Hub GitHub Page](https://github.com/FAR-Lab/Interactive-Lab-Hub) under [Lab 2/screen_clock.py](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/Fall2022/Lab%202/screen_clock.py)

# 3. Building the User Interface for the System

The biggest concern for this project was not to simply create a functional product but also take into account the design and user interface principles that was taught in the class. We were able to use the knowledge gained from the class to create a user interface that was both functional and aesthetically pleasing. 

<p align="center">
    <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/UIBoard.png" width="200" title="board">
</p>

<p align="center">
    <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/case.png" width="400" title="board">
</p>

We were able to source and acquire a pre-built model for the very popular Raspberry Pi from [here](https://www.thingiverse.com/thing:922740). However, since we had additional hardware and a display to be mounted and visible to the user, the model was modified. Ideally, with enough time, we would create a custom model in Fusion360 for the Raspberry Pi and the additional hardware but in this case, we 3D printed the model as is and sawed out the necessary space for the display. The extra hardware, ie. the GPS module, was simply stuck on the case with sticky tape. The resulting model is shown below:

<p align="center">
    <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/boardgif.gif" width="400" title="board">
</p>

# 4. Cloud Server Development

The main aim of this project is to provide useful insights and data in a visually appealing manner to a user. Using GPS coordinates collected during a run, one can extract a huge amount of workout insights including workout path, average pace, total distance, time taken and more.

To complete this task, a server was rented from [Linode](https://www.linode.com), a platform providing cloud based services. Linux based servers running other Linux distros can also be rented from other providers such as [DigitalOcean](https://www.digitalocean.com/products/droplets), [Amazon Web Services](https://aws.amazon.com/ec2/?nc2=h_ql_prod_cp_ec2), [Microsoft Azure](https://azure.microsoft.com/en-gb/services/virtual-machines/), [Google Cloud](https://cloud.google.com/compute), etc. Most providers offer free credits for the first few months.

## 4.1 Server Setup

The server in question is a Linux based Ubuntu server running a Node.js application to accept RESTful API requests.

The following steps will guide you through the process of setting up a Node.js server on a Linux server.

1. [SSH(Secure Shell)](https://phoenixnap.com/kb/ssh-to-connect-to-remote-server-linux-or-windows) into the server using the command:
    ```bash
    ssh root@[IPv4 address]
    ```

2. Install NVM which is the [Node Version Manager](https://github.com/nvm-sh/nvm) using the command:
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    ```

3. Reload the bash preferences with the command:
    ```bash
    source ~/.bashrc
    ```

4. Install the correct Node.js version:
    - Get the latest available version:
        ```bash
        nvm ls-remote
        ```
    
    - Install the specified Node.js version:
        ```bash
        nvm install 18.0.0
        ```

5. Install [PM2](https://pm2.keymetrics.io) which is a Node.js application Process Manager using the command:
    ```bash
    npm i -g pm2
    ```

After completing the above steps, the server is ready to host a Node.js application.

The above steps were sourced from the following [YouTube Video by CodeBubb](https://www.youtube.com/watch?v=fJ4x00SR7vo).

## 4.2. Backend Node.js Application Setup

For this project, we will be using a Node.js server to collect, format and store the GPS data that is streamed from the Raspberry Pi to a JSON file. The data for each run is stored in an array where each index, representing a run, contains an object with the following properties:

```json
{
    "runid": 1,
    "lat": ["lat1", "lat2", "lat3", ...],
    "lon": ["lon1", "lon2", "lon3", ...]
}
```

The logic of the backend is as follows:

1. A '/newrun' endpoint creates a new runid and stores it in the run.json file with an empty latitude and longitude list.

```javascript
app.get('/newrun', (req, res) => {
    const main = async () => {

        var data1 = await fs.readFile('/root/src/run.json', 'utf8');
        data1 = JSON.parse(data1)
        lastrun = data1[data1.length-1]
        
        var data2 = {
            "runid": (parseInt(lastrun.runid)+1),
            "lat": [],
            "lon": []
        }
        data1.push(data2)

        await fs.writeFile('/root/src/run.json', JSON.stringify(data1));

        console.log('New Run Created')
        res.send(String(parseInt(lastrun.runid)+1))

    }
    main()
});
```

2. At every half a second interval, a GET request is made to the '/append' endpoint where runid, latitude, and longitude data is passed as parameters. The server takes the data and appends it to the corresponding runid in the run.json file.

```javascript
app.get('/append/:runid/:lat/:lon', (req, res) => {
    const main = async () => {

        var runid = req.params.runid
        var lat = req.params.lat
        var lon = req.params.lon

        var data1 = await fs.readFile('/root/src/run.json', 'utf8');
        data1 = JSON.parse(data1)

        var newlat = data1[data1.length-1].lat
        var newlon = data1[data1.length-1].lon
        
        newlat.push(parseFloat(lat))
        newlon.push(parseFloat(lon))

        var data2 = {
            runid: parseInt(runid),
            lat: newlat,
            lon: newlon
        }

        data1.splice(-1)
        data1.push(data2)

        await fs.writeFile('/root/src/run.json', JSON.stringify(data1));
        var data = await fs.readFile('/root/src/run.json', 'utf8');
        myObject = JSON.parse(data)
        
        console.log("Latitude: " + lat + ", Longitude: " + lon)
        res.send('Done')

    }
    main()
});
```

3. When the user wishes to access the web dashboard via the index.html page, the website accesses the '/getnumruns' endpoint to get the number of runs that have been stored in the run.json file. This is used to display the number of runs in the dropdown menu for a selection of runs.

```javascript
app.get('/getnumruns', (req, res) => {
    const main = async () => {

        var runData = await fs.readFile('/root/src/run.json', 'utf8');
        runData = JSON.parse(runData)

        res.header("Access-Control-Allow-Origin", "*")
        res.json(
            {
                numRuns: parseInt(runData.length)
            }
        )

    }
    main()
});
```

4. When the user wishes to access the data and metrics of a specific run, the dashboard creates a GET request to the 'analyze-run' endpoint with the runid as a parameter. The server then reads the run.json file and returns the latitude and longitude list of data for the runid to the frontend. This is all then processed on the client side using the Google Maps API for JavaScript.

```javascript
app.get('/analyze-run/:runNum', (req, res) => {
    const main = async () => {

        var runNum = req.params.runNum

        var runData = await fs.readFile('/root/src/run.json', 'utf8');
        runData = JSON.parse(runData)

        for(let i = 0; i < runData.length; i++) {
            if(runData[i].runid == runNum){
                var retRunID = runData[i].runid
                var retLat = runData[i].lat
                var retLon = runData[i].lon
            }
        }

        res.header("Access-Control-Allow-Origin", "*")
        res.json(
            {
                runid: retRunID,
                lat: retLat,
                lon: retLon
            }
        )

    }
    main()
});
```

All of this code is stored in [app.js](https://github.com/abhisheknair10/IDD-Final-Project/blob/main/server/app.js) in this GitHub repository.

The [Express](https://expressjs.com) framework is Node.js compatible framework to create and serve REST API endpoint requests created by clients. Hence, we need to install it using the command:

```bash
npm install express
```

Now the application is ready to run with the following commands:

1. To run the application using node:
    ```bash
    node app.js
    ```
2. To run the application using PM2:
    ```bash
    pm2 start app.js
    ```

# 5. Client Side Development

## 5.1. Frontend Web Dashboard Setup

The frontend of this application for viewing the runs on a dashboard is hosted on Linode and is built using HTML, CSS, and JavaScript. The HTML and CSS files are stored in [index.html](https://github.com/abhisheknair10/IDD-Final-Project/blob/main/frontend/index.html)

## 5.2. Google Maps JavaScript API
Displaying the workout data on a map as path on the map was possible with the help of Google's [Maps JavaScript API](https://developers.google.com/maps/documentation/javascript).

<p align="center">
    <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/dashboard.png" width="800" title="gmapi">
</p>

With a [Google Cloud Account](https://cloud.google.com) created, navigate to 'Credentials' and create a new API key. The next step is to enable the Maps JavaScript API under 'Enabled APIs & Services'.

The API is now initialized and accessible.

The map is initialized using the following code:

```js
var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 17,
    center: new google.maps.LatLng(latitude, longitude),
    mapTypeId: "terrain",
});
```

The coordinates are marked on the map using the following code:
```js
const runPath = new google.maps.Polyline({
    path: runCoords,
    geodesic: true,
    strokeColor: "#e34444",
    strokeOpacity: 1.0,
    strokeWeight: 4,
});

runPath.setMap(map);
```

Marking and plotting lines on the map in detail can be found in the [source code](https://github.com/abhisheknair10/IDD-Final-Project/blob/main/frontend/index.html).

Access the dashboard by simply downloading the HTML file and opening it in your browser.

# 6. Testing, Results and Conclusions

## 6.1. Testing and Results

The above system was tested by the developers and here is the result:

[<img alt="alt_text" width="800px" src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/img.png" />](https://drive.google.com/file/d/1ktqxDswKMsTHWC6RikK0EJRZScrPKKHv/view?usp=sharing)

The final device was built and tested with a user here:

<p align="center">
    <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/user.gif" width="400" title="board">
</p>

[<img alt="alt_text" width="800px" src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/img.png" />](https://drive.google.com/file/d/1gSbc73K5WCHTG4GuZ3Zx8EB3bQomEP5Q/view?usp=sharing)


## 6.2. Pitfalls and Issues

While doing this project, we encountered some technical issues with the hardware and software. Some of the issues we faced are listed below:

1. The biggest issue we faced was getting the GPS module interfaced with the Raspberry Pi. The Neo 6M that we are using this project is a newer version with a micro USB port and we wanted to make use of that port as opposed to using the RX and TX along with Vcc and GRND port due to it's simplicty and robustness. For some context, the Vcc (Voltage In) port and GRND (Ground) port essentially allow for the GPS module to get power from any device. The RX and TX ports are Receiver and Transmission ports for the GPS module to essentially receive and transmit data to and from a microcontroller or in this case, the Raspberry Pi. Hence, finding documentation to interface the module required running a lot of commands to tap into the hardware to understand what ports were doing which function. Thankfully, Vik has a background in Electrical and Computer Engineering and extensive experience with hardware and was able to debug the hardware issues and get the GPS module interfacing working.

2. The GPS module is able to function and output accurate latitude and longitude coordinates by receiving and decoding signals sent by satellites over the sky. This is why the GPS doesn't function well indoors. Generally, when first used, the module requires an open and clear view of the sky to get an inital lock on the satellites. This can sometimes take anywhere from 5 to 30 minutes. During our project, the module ended up taking around 20 mins to lock during which we were wondering whether we have a faulty device, it's not getting a signal due to a lack of a clear view of the sky, or if the signals sent out by US satellites were not compatible with our module. Thankfully, we were able to get the module working and it was able to output accurate coordinates.

3. Initially, the frontend of the application was hosted on GitHub Pages, a service provided by GitHub to host static websites. However, since the API endpoint for getting the recorded GPS sat in a non secure (HTTP as opposed to HTTPS) and the data was being requested from a HTTPS site, the browser was blocking the request. Converting our endpoint from a HTTP to a HTTPS endpoint requires the purchase of a domain name and an SSL certificate which usually costs in total a few hundred dollars. Since this is project and more or less a proof of concept, we decided to download the HTML file locally and run it on the browser instead of hosting it on GitHub Pages.

## 6.3. Conclusions

Overall, we were able to successfully build a GPS tracking application that can be used to track runs and other outdoor activities. The application is able to record the GPS coordinates of the user and store it in a JSON file. The data is then served to the frontend dashboard which displays the data on a map. The application is able to run on a Raspberry Pi and can be used to track runs and other outdoor activities.