//jshint esversion:6

const express = require("express");
const { spawn } = require('child_process');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(express.static(__dirname));


app.get('/', (req, res) => {
  res.sendFile(__dirname +'/templates/index.html');
});


app.post('/process_link', async (req, res) => {
  const link = req.body.link;
  const raceID = req.body.r;
  var raceInfo;
  
  async function getData() {
    try {
      const newlink = 'https://www.live-timing.com/includes/aj_race.php?r='+ raceID + '&&m=1&&u=5'
      console.log("SENT LINK: ", newlink);
      const response = await fetch(newlink, {
        method: 'GET',
        headers: {'Accept': '*/*',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
                 },
      });
      if (!response.ok) {
        throw new Error(`HTTP error. Status: ${response.status}`)
      }
      const info = await response.text();
      return info
  
    } catch (error) {
      console.error('Error:', error);
    } 
  }

  try {
    raceInfo = await getData(); // Await the result of getData
    // console.log(raceInfo); // Now you can access raceInfo

    // Processing the response into readable chunks using same process as original Live Timing website
    var comps = new Array();
    var discipline;
    var type2;
    var lines = raceInfo.split("|"); linesLength = lines.length; 
    var lineCount = 0;
    while (lineCount < lines.length) {
      var items = lines[lineCount].split("=");
      if (items[0]=="b") {
        var who = -1
        if (items[1] != '' && comps.length > 0){
          if (comps[0].bib == ''){
            comps.length = 0
          }
          var compsLength = comps.length
          for (var i=0; i<compsLength; i++){
            if (comps[i].bib == items[1]){ 
              who = i
            }
          }
        }
        if (who == -1) {
          who = comps.length;
          comps[who] = {rank: "", bib: "", name: "", r1: "", r1AsInt: 0, r1Rank:"", r2:"", r2AsInt:0, r2Rank:"", total:"", totalAsInt:2147483500, fnumber:"", fpoints:0}
          comps[who].bib = items[1]
        }
        
      } 
      else if (items[0] == "m") comps[who].name = items[1]
      else if (items[0] == "fn") comps[who].fnumber = items[1]
      else if (items[0] == "fp") comps[who].fpoints = items[1]
      else if (items[0] == "r1") {
        comps[who].r1 = items[1]
        comps[who].r1AsInt = items[2]
      }
      else if (items[0] == "r2") {
        comps[who].r2 = items[1]
        comps[who].r2AsInt = items[2]
      }
      else if (items[0] == "tt") {
        comps[who].total = items[1]
        if (type2 == 'Best')
        comps[who].totalAsInt = Math.min(comps[who].r1AsInt,comps[who].r2AsInt)
        else	if (comps[who].r1AsInt < 2147483500 && comps[who].r2AsInt < 2147483500)
        comps[who].totalAsInt = 1 * comps[who].r1AsInt + 1 * comps[who].r2AsInt
        else
        comps[who].totalAsInt = 2147483500
      }
      else if (items[0] == "hT") {
        discipline = items[1]
        type2 = items[2]
      }
      lineCount++
    }
  
    // console.log(JSON.stringify(comps), discipline);
  

    // Spawn a Python process and capture its output
    const pythonProcess = spawn('python3', ['penalty_calculation.py', JSON.stringify(comps), discipline]);

    let output = '';

    pythonProcess.stdout.on('data', (data) => {

      output += data.toString(); //new

      pythonProcess.on('close', (code) => {
        if (code != 0) {
          return res.status(500).send('Python process failed'); 
        }
        try {
          var jsonObject = JSON.parse(output); // Parse output
          return res.json({ result: jsonObject });   // Send the Python program's output to the frontend
        } catch (parseError) {
            return res.status(500).send('Failed to parse Python output'); // Handle parsing error
        }
      });
    });
  } catch (error) {
      console.error('Error processing request:', error);
      res.status(500).send('Internal Server Error'); 
  }
});


app.listen(port, () => {
    console.log("Server started on port", port);
});