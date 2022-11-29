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

# Table of Contents

<div align="center">

| No      |  Title 
| :---:   | :---: 
| 1.      | [About the Hardware](https://github.com/abhisheknair10/IDD-Final-Project#1-about-the-hardware)
| 2.      | [The Run Tracking Software on the Raspberry Pi](https://github.com/abhisheknair10/IDD-Final-Project#2-the-run-tracking-software-on-the-raspberry-pi)
| 3.      | [Cloud Server Development](https://github.com/abhisheknair10/IDD-Final-Project#3-cloud-server-development)
| 4.      | [Client Side Development](https://github.com/abhisheknair10/IDD-Final-Project#4-client-side-development)

</div>

To understand how the different parts of this project and different services communicate with each other to create a valuable application, below is a diagram of the app architecture.

<p align="center">
    <img src="https://github.com/abhisheknair10/IDD-Final-Project/blob/main/Assets/App%20Architecture.png" width="600" title="IDD Slide">
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

2. Identify all the ports on the Raspberry Pi and find the one that is associated with the GPS module:
    ```bash
    ```bash
    ls -l /dev/tty*
    ```
For our specific device, the port was /dev/ttyAMA0.

This port needs to be noted down when running the python file to read the GPS data from the correct port at a baud rate of 9600.


# 2. The Run Tracking Software on the Raspberry Pi

To be added...

# 3. Cloud Server Development

The main aim of this project is to provide useful insights and data in a visually appealing manner to a user. Using GPS coordinates collected during a run, one can extract a huge amount of workout insights including workout path, average pace, total distance, time taken and more.

To complete this task, a server was rented from [Linode](https://www.linode.com), a platform providing cloud based services. Linux based servers running other Linux distros can also be rented from other providers such as [DigitlOcean](https://www.digitalocean.com/products/droplets), [Amazon Web Services](https://aws.amazon.com/ec2/?nc2=h_ql_prod_cp_ec2), [Microsoft Azure](https://azure.microsoft.com/en-gb/services/virtual-machines/), [Google Cloud](https://cloud.google.com/compute), etc. Most providers offer free credits for the first few months.

## 3.1 Server Setup

The server in question is a Linux based Ubuntu server running a Node.js application to accept RESTful API requests.

The following steps will guide you through the process of setting up a Node.js server on a Linux server.

1. SSH(Secure Shell) into the server using the [command](https://phoenixnap.com/kb/ssh-to-connect-to-remote-server-linux-or-windows):
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

The above steps were sourced from the following [YouTube Video](https://www.youtube.com/watch?v=fJ4x00SR7vo).

## 3.2. Backend Node.js Application Setup
___

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

3. When the user wishes to access the web dashboard via GitHub Pages, the website accesses the '/getnumruns' endpoint to get the number of runs that have been stored in the run.json file. This is used to display the number of runs in the dropdown menu for a selection of runs.

```javascript
app.get('/getNumRuns', (req, res) => {
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

Since we are using the Express framework, we need to install it using the command:

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

# 4. Client Side Development