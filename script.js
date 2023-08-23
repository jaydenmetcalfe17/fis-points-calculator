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
        

        const data = await response.json()

    
        var scores = Object.keys(data.result).map((key) => [key, data.result[key]]);
        var table = document.getElementById('result')

        for (var i=0; i<scores.length; i++) {
            var row = table.insertRow(-1)
            var cell1 = row.insertCell(0)
            var cell2 = row.insertCell(1)
            var cell3 = row.insertCell(2)
            var score = scores[i].toString()

            var broken = score.split(",")
            
            cell1.innerHTML = broken[1]
            cell2.innerHTML = broken[0]
            cell3.innerHTML = broken[2]
        }
    

    } catch (error) {
        console.error('Error:', error);
    }
});
