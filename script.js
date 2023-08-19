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
        const data = await response.json();
        console.log("response: ", data)
        document.getElementById('result').textContent = data.result;
    } catch (error) {
        console.error('Error:', error);
    }
});
