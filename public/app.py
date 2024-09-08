from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Travel times in hours (from city to destination)
travel_times = {
    'Ahmedabad': {'Gir': 6, 'Somnath': 8, 'Vadodara': 1.5, 'Rajkot': 3, 'Surat': 3},
    'Surat': {'Gir': 6.5, 'Somnath': 8.5, 'Vadodara': 2, 'Rajkot': 4, 'Ahmedabad': 3},
    'Vadodara': {'Gir': 7, 'Somnath': 9, 'Rajkot': 3, 'Surat': 2, 'Ahmedabad': 1.5},
    'Rajkot': {'Gir': 5, 'Somnath': 7.5, 'Vadodara': 3, 'Surat': 4, 'Ahmedabad': 3}
}

# Tourist spots
tourist_spots = {
    'Ahmedabad': ['Sabarmati Ashram', 'Kankaria Lake', 'Adalaj Stepwell', 'Sidi Saiyyed Mosque'],
    'Gir': ['Gir National Park', 'Devalia Safari Park', 'Kamleshwara Temple', 'Sinh Sadan'],
    'Somnath': ['Somnath Temple', 'Bhalka Tirth', 'Prabhas Patan Museum', 'Somnath Beach'],
    'Vadodara': ['Laxmi Vilas Palace', 'Sayaji Garden', 'Baroda Museum & Picture Gallery', 'Mandvi Gate'],
    'Rajkot': ['Mahatma Gandhi Museum', 'Kaba Gandhi No Delo', 'Rajkumar College', 'Watson Museum'],
    'Surat': ['Surat Castle', 'Dutch and Armenian Cemeteries', 'Sarthana Nature Park', 'Gopi Talav']
}

# Food recommendations
food_recommendations = {
    'Ahmedabad': ['Khaman', 'Dhokla', 'Patra'],
    'Gir': ['Kathiawadi Thali', 'Farsan', 'Gujarati Kadhi'],
    'Somnath': ['Gujarati Thali', 'Farsan', 'Khadi'],
    'Vadodara': ['Undhiyu', 'Khadi', 'Handvo'],
    'Rajkot': ['Kathiawadi Thali', 'Farsan', 'Khandvi'],
    'Surat': ['Locho', 'Surati Undhiyu', 'Surti Khaman']
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    itinerary_data = request.args
    try:
        budget = int(itinerary_data.get('budget_usd', '0')) * 75
    except ValueError:
        budget = 0  # Default value if conversion fails

    return render_template(
        'result.html',
        destination=itinerary_data.get('destination', 'Unknown'),
        starting_city=itinerary_data.get('starting_city', 'Unknown'),
        nights=itinerary_data.get('nights', '0'),
        persons=itinerary_data.get('persons', '0'),
        start_date=itinerary_data.get('start_date', 'Unknown'),
        itinerary=itinerary_data.get('itinerary', '<p>Your custom itinerary will be shown here.</p>'),
        travel_options='Available travel options: Bus, Train, Road',
        food_recommendations=', '.join(food_recommendations.get(itinerary_data.get('destination', 'Unknown'), ['No recommendations'])),
        accommodation_options='Hotels: Budget, Mid-range, Luxury',
        budget=budget
    )

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    data = request.get_json()

    starting_city = data.get('starting_city', 'Unknown')
    destination = data.get('destination', 'Unknown')
    nights = data.get('nights', '0')
    persons = data.get('persons', '0')
    start_date = data.get('start_date', 'Unknown')
    
    try:
        nights = int(nights)
        start_time = datetime.fromisoformat(start_date)
    except ValueError:
        return jsonify({'error': 'Invalid input data'}), 400

    travel_time = travel_times.get(starting_city, {}).get(destination, 0)
    arrival_time = start_time + timedelta(hours=travel_time)

    itinerary = []
    current_time = arrival_time + timedelta(minutes=30)  # Adding 30 mins for rest

    spots = tourist_spots.get(destination, [])
    
    if nights <= 5:
        spots = spots[:4]
    elif nights <= 10:
        spots = spots[:6]
    elif nights <= 20:
        spots = spots[:12]
    else:
        spots = spots[:15]
    
    for idx, spot in enumerate(spots):
        visit_time = current_time + timedelta(hours=1)
        itinerary.append(f"{visit_time.strftime('%H:%M')} - {spot}")
        current_time = visit_time + timedelta(hours=1)  # 1 hour for each spot
    
    itinerary.append(f"{current_time.strftime('%H:%M')} - Return to hotel")
    
    return jsonify({
        'starting_city': starting_city,
        'destination': destination,
        'nights': nights,
        'persons': persons,
        'start_date': start_date,
        'itinerary': '<br>'.join(itinerary),
        'food_recommendations': ', '.join(food_recommendations.get(destination, ['No recommendations'])),
        'budget_usd': data.get('budget_usd', '0')
    })

if __name__ == '__main__':
    app.run(debug=True)
