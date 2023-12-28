# FIS Points Calculator #
## Description ##
Currently, there are no public applications where racers can see their scores immediately. They must wait hours for the results to be calculated and posted. With this application, the problem is solved. The user can input a link (from live-timing.com) into the website while using Chrome browser. The program then sends the link to the Python file which uses Selenium to scrape the website. The extracted information is processed by the program and calculates the score of each racer using the FIS Race points and FIS penalty calculations. The results are returned and then displayed on the webpage for the user.

**Only for SL or GS races, not designed for single run events such as Super G or Downhill**\
**Link must be from live-timing.com**

## Installation ##
```
npm install body-parser express child_process nodemon
```
OR
```
npm install
```


## Usage ##
To start the server run the following command:
```
nodemon app.js
```
Currently, the program requires Chromedriver to be installed on the local device as Selenium Manager was not automatically downloading the appropriate driver. Please ensure to update the correct path to the Chromedriver in penalty_calculation.py

## Last Updated ##
December 27, 2023