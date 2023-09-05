# FIS Points Calcultor #
## Description ##
Currently, there are no public applications where racers can see their scores immediately. They must wait hours for the results to be calculated and posted. With this application, the problem is solved. The user can input a link (from live-timing.com) into the website while using Chrome browser. The program then sends the link to the Python file which uses Selenium to scrape the website. The extracted information is process by the program, and calculates the score of each racer using the FIS Race points and FIS penalty calculations. The results are returned and then displayed on the webpage for the user.

```
**Compatible with Chrome version 114**
**Only for SL or GS races, not designed for single run events such as Super G or Downhill**
**Link must be from live-timing.com**
```

## Installation ##
```
npm install body-parser express child_process nodemon
```


## Usage ##
To start the server run the following command:
```
nodemon app.js
```


