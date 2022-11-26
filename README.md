# IDD-Final-Project Documentation

Collaborators:

1. Abhishek Nair - an464@cornell.edu
2. Vikram Pandian - vip6@cornell.edu

Introduction

Internet of Things and Interactive Devices is the field of technology that deals with physical objects with computational capabilties, sensors and actuators that can connect to any form of network, including the internet, to exchange data with other devices, servers or the cloud.

This project aims to make use of this concept to build a GPS tracker based system for running enthusiasts to track their runs and workouts. A runner will be able to take the device with them while on a run. During this time, the Raspberry Pi will stream the GPS data as well as time data to a remote server via WiFi or Cellular. The server will then store this data and allow the user to view it on a web interface. The user will be able to view the route they took on a map, as well as the time it took them to complete the run. The user will also be able to view their average speed, distance, and other statistics. The user will also be able to view their previous runs and compare them to each other.

The aim of this assignment is to:

1. Build and connect the hardware components
2. Receive and process GPS data from the GPS module
3. Send GPS data to a remote server
4. Serve the data on a web dashboard

Table of Contents

<<<<<<< HEAD
| No      |  Title 
| :---:   | :---: 
| 1.      | [INSERT TITLE HERE]()
| 2.      | [INSERT TITLE HERE]()
| 3.      | [INSERT TITLE HERE]()
| 4.      | [INSERT TITLE HERE]()
=======
A separate part of the dashboard will also display the localities and neighbourhoods the runner has visited. In such a scenario, a runner may wish to choose which route to take next after visiting certain neighbourhoods.

The Raspberry Pi will also be able to use data collected from an accelerometer to detect when the user has had a fall. This fall detection can be used to contact local emergency services as well as a personal emergency contact such as family members in case of an injury.

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



## Parts Needed

The parts needed would be:

1. 1 x Raspberry Pi
2. 1 x GPS Module
3. 1 x Accelerometer
4. 1 x Phone only for cellular connectivity

## Risks/Contingencies

The only risk associated with this project is the lack of execution for the fall detection feature. This is because designing a machine learning model or a neural network to detect a fall may not be as straightforward as we think.

A contingency plan for this would be to use a pre-trained model for fall detection. This would be a good option because we would not have to spend time training a model and can instead focus on the other features of the project. 

In a scenario where we are unable to find a pre-trained model, we can instead make use of buttons programmed with quick actions for the user to press in the scenario where they would like to contact emergency services.

## Fallback Plan

The fallback plan is to build a camera based system to be placed on the back of cyclists to detect and warn its user of approaching vehicles and other cyclists. Many a times, cyclists are not aware of the activity happening behind them but may be very useful to take corrective action in different scenarios. For example, a cyclist may decide not to drive towards the road when they know a large heavy vehicle like a truck is approaching from behind and going to pass by them.

This is a good fallback plan since my teammate and I are relatively well experienced in computer vision and machine learning and implementing this in the time frame would be possible and a good learning experience.
>>>>>>> 182a8047262ba752b4826f92da982d61fcf8c715
