from src.predict import predict

input_data = {
    'Airline': 'AA',
    'Origin': 'JFK',
    'Destination': 'LAX',
    'ScheduledDeparture': '2024-05-15 10:00:00',
    'Distance': 3000
}

print(predict(input_data))