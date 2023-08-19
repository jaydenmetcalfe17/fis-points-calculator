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


app.post('/process_link', (req, res) => {
  const link = req.body.link;

  // Spawn a Python process and capture its output
  const pythonProcess = spawn('python3', ['penalty_calculation.py', link]);

  let output = '';

  pythonProcess.stdout.on('data', (data) => {
    const dataString = data.toString('utf8'); // Convert Buffer to string
    
    const jsonObject = JSON.parse(dataString); // Parse JSON
    console.log('Received JSON object:', jsonObject);
    
    output += jsonObject;
  });


  pythonProcess.on('close', (code) => {
      // Send the Python program's output to the frontend
      res.json({ result: output });
  });
});


  

app.listen(port, () => {
    console.log("Server started on port", port);
});