document.getElementById('linkForm').addEventListener('submit', async function(event) {
  event.preventDefault(); // Prevent default form submission

  // Get the input link
  const link = document.getElementById('linkInput').value;
  const url = new URL(link)
  const params = new URLSearchParams(url.search)
  const r = params.get('r')
  console.log('Link submitted:', link);

  // Send the link to the Python program using an API call
  try {
        const response = await fetch('/process_link', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ link: link, r: r })
        });

        const data = await response.json()
    
        var scores = Object.keys(data.result).map((key) => [key, data.result[key]]);
        var table = document.getElementById('result')
        var rank = 1

        for (var i=0; i<scores.length; i++) {
            var row = table.insertRow(-1)
            var cell1 = row.insertCell(0)
            var cell2 = row.insertCell(1)
            var cell3 = row.insertCell(2)
            var cell4 = row.insertCell(3)
            var score = scores[i].toString()

            var broken = score.split(",")
            
            cell1.innerHTML = rank
            cell2.innerHTML = broken[1]
            cell3.innerHTML = broken[0]
            cell4.innerHTML = broken[2]
            
            rank += 1
        }
    

    } catch (error) {
        console.error('Error:', error);
    }
});
