document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        recency: formData.get('recency'),
        frequency: formData.get('frequency'),
        monetary: formData.get('monetary'),
        time: formData.get('time')
    };

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(data)
    })
    .then(response => response.json())
    .then(result => {
        let resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<p>Prediction: ${result.prediction}</p>`;
        if (result.prediction === 'Will donate') {
            resultDiv.innerHTML += `<p>Estimated months until next donation: ${result.next_donation}</p>`;
        }
    })
    .catch(error => console.error('Error:', error));
});
