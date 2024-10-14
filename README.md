# FIS Points Calculator #
## Description ##
Currently, there are no public applications where racers can see their scores immediately. They must wait hours for the results to be calculated and posted. With this application, the problem is solved. The user can input a link (from live-timing.com) and the program makes a request using that link to return relevant information about the racers and their times and existing FIS points. It then sends the race info to the Python file. The extracted information is processed by the program and calculates the score of each racer using the FIS Race points and FIS penalty calculations. The results are returned and then displayed on the webpage for the user.

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
Then you can access locally via local host 3000 in your browser

## Last Updated ##
October 14, 2024