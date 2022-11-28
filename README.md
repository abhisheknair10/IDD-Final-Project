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
| 1.      | [About the Hardware]()
| 2.      | [The Run Tracking Software on the Raspberry Pi]()
| 3.      | [Cloud Server Development]()
| 4.      | [Client Side Development]()

</div>

# 1. About the Hardware

# 2. The Run Tracking Software on the Raspberry Pi

# 3. Cloud Server Development
The main aim of this project is to provide useful insights and data in a visually appealing manner to a user. Using GPS coordinates collected during a run, one can extract a huge amount of workout insights including workout path, average pace, total distance, time taken and more. 

To complete this task, a server was rented from [Linode](https://www.linode.com), a platform providing cloud based services. Linux based servers running other Linux distros can also be rented from other providers such as [DigitlOcean](https://www.digitalocean.com/products/droplets), [Amazon Web Services](https://aws.amazon.com/ec2/?nc2=h_ql_prod_cp_ec2), [Microsoft Azure](https://azure.microsoft.com/en-gb/services/virtual-machines/), [Google Cloud](https://cloud.google.com/compute), etc. Most providers offer free credits for the first few months.

## 3.1. Server Setup
___

For this project, we will be using a Node.js server to collect, format and store the GPS data that is streamed from the Raspberry Pi to a JSON file. The data is stored in the following format:

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

All of this code is stored in [app.js]() in this GitHub repository.

However, to run Node.js on a Linux server requires installing certain tools and libraries.The following steps will guide you through the process of setting up a Node.js server on a Linux server.

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

# 4. Client Side Development