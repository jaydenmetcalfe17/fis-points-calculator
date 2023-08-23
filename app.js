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

    var jsonObject = JSON.parse(data)
    
    output += jsonObject;

    pythonProcess.on('close', (code) => {
      // Send the Python program's output to the frontend
      
      res.json({ result: jsonObject });
    });
  });
});

app.listen(port, () => {
    console.log("Server started on port", port);
});