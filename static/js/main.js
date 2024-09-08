document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('itinerary-form');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            starting_city: formData.get('starting_city'),
            nights: formData.get('nights'),
            persons: formData.get('persons'),
            destination: formData.get('destination'),
            start_date: formData.get('start_date'),
            budget_usd: formData.get('budget_usd')
        };

        fetch('/generate_itinerary', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `
                <h2>Destination: ${data.destination}</h2>
                <p><strong>Starting City:</strong> ${data.starting_city}</p>
                <p><strong>Nights:</strong> ${data.nights}</p>
                <p><strong>Persons:</strong> ${data.persons}</p>
                <p><strong>Start Date:</strong> ${data.start_date}</p>
                <p><strong>Travel Options:</strong> ${data.travel_options}</p>
                <p><strong>Food Recommendations:</strong> ${data.food_recommendations}</p>
                <p><strong>Accommodation Options:</strong> ${data.accommodation_options}</p>
                <p><strong>Estimated Budget (INR):</strong> ${data.budget}</p>
                <div>${data.itinerary}</div>
            `;
        })
        .catch(error => console.error('Error:', error));
    });
});
