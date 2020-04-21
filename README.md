# Hikvision Events

Hikvision Events is an interface between a Hikvision NVR and SmartThings that allows events, such as line crossings and motion detection from cameras, to be available to Smartthings as sensors.

# Installation

Installation involves 2 parts:
    1) Installing the SmartApp and associated Device Handler
    2) Setting up the HikvisionEventsServer python script

Installing the SmartApp and associated Device Handler:
    1) Log into your Smartthings IDE via a web browser
    2) Select *My SmartApps* and click on the *Settings* button
    3) Now add a new repository with *Owner* rtorchia, *Name* Smartthings-Hikvision-Events and *Branch* master. Select Save when done.
    4) Tap on the *Update from Repo* button and select the Hikvision-Events repo.
    5) Select the Hikvison Motion Sensors application and install it.

Repeat these steps 4 and 5 for installing the device handler under *My Device Handlers*. Also, don't forget to enable Oauth for the SmartApp.

Hikvisioneventsserver Setup:
    1) Edit the hikvisionevents.cfg file.
        (a) Enter the IP address and login information for your Hikvision NVR.
        (b) Change the Smartthings host to where your IDE resides (usually the web URL of your IDE). Add the accessToken and appkey/appID of the SmartApp. To find it, open your IDE and go to Locations, then select the smartapps link in the location you installed the app, then find it in the list and click on its name. The access token is found in the *Application State*. You can find all three parameters in the endpoint field of the form *https://{{host}}:443/api/token/{{accessToken}}/smartapps/installations/{{appId}}/*
        (c) Edit the names of the cameras attached to your NVR.
    2) Run the python script.  You can setup events and alarms in your Hikvision NVR using its web interface or the client software. When an event is first triggered it will be added automatically as a device to Smartthings.
