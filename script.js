document.getElementById('linkForm').addEventListener('submit', async function(event) {
  event.preventDefault(); // Prevent default form submission

  // Get the input link
  const link = document.getElementById('linkInput').value;
  console.log('Link submitted:', link);

  // Send the link to the Python program using an API call
  try {
        const response = await fetch('/process_link', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ link: link })
        });
        
        //const data = await response.json();
        const data = await response.json()

    
        var scores = Object.keys(data.result).map((key) => [key, data.result[key]]);

        //document.getElementById('result').textContent = JSON.stringify(data.result);
        //document.getElementById('result').textContent = scores
        var table = document.getElementById('result')

        for (var i=0; i<scores.length; i++) {
            var row = table.insertRow(-1)
            var cell = row.insertCell(0)
            var score = scores[i]
            cell.innerHTML = score
          }
    

    } catch (error) {
        console.error('Error:', error);
    }
});
