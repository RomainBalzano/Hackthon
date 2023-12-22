#!/usr/bin/env python3

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

usage_data = {
    "Kitchen": {"Microwave": 0, "Oven": 0, "Fans": 0, "Lampe": 0, "total": [0, 0, 0]},
    "Garage": {"Car": 0, "Lampe": 0, "total": [0, 0, 0]},
    "LivingRoom": {"Lampe": 0, "TV": 0, "PlayStation": 0, "total": [0, 0, 0]},
    "BedRoom": {"Lampe": 0, "total": [0, 0, 0]},
}

grade_room = {
    "Kitchen": 1,
    "Garage": 1,
    "LivingRoom": 1,
    "BedRoom": 1,
}

averages = {}

def linear(x, x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    y = slope * x + intercept
    return y

def getPowerEdf(start_time, end_time):
    start_hour, start_minute = map(int, start_time.split(":"))
    end_hour, end_minute = map(int, end_time.split(":"))

    print(str(start_hour) + " " + str(end_hour))
    x_values = list(range(start_hour, end_hour + 1))
    print(x_values)

    powers = [
        linear(x, 0, 100, 12, 3500) if 0 <= x <= 12
        else linear(x, 12, 3500, 15, 2000) if 12 < x <= 15
        else linear(x, 15, 2000, 19, 5000) if 15 < x <= 19
        else linear(x, 19, 5000, 23, 100)
        for x in x_values
    ]

    return max(powers)

def assign_grade(Number, Critical, tolerance=500):
    difference = Critical - Number
    if difference <= tolerance or difference < 0:
        return 0
    elif difference <= 2 * tolerance:
        return 0.25
    elif difference <= 3 * tolerance:
        return 0.5
    elif difference <= 4 * tolerance:
        return 0.75
    else:
        return 1

def calculate_time_difference(start_time, end_time):
    start_hour, start_minute = map(int, start_time.split(':'))
    end_hour, end_minute = map(int, end_time.split(':'))
    start_total_minutes = start_hour * 60 + start_minute
    end_total_minutes = end_hour * 60 + end_minute
    if end_total_minutes < start_total_minutes:
        end_total_minutes += 24 * 60
    return end_total_minutes - start_total_minutes

@app.route('/api/power/', methods=['GET', 'POST'])
def index():
    global averages
    if request.method == 'POST':
        try:
            with open('pow.json') as f:
                machines = json.load(f)
            json_data = request.get_json()
            for room, devices in json_data.items():
                for device, timings in devices.items():
                    start_time, end_time = timings
                    WorstPower = getPowerEdf(start_time, end_time)
                    time_needed = calculate_time_difference(start_time, end_time)
                    if device == "total":
                        break
                    power = machines[device]["power"]
                    energy = time_needed * power
                    usage_data[room][device] += energy
                    usage_data[room]["total"][0] += energy
                    usage_data[room]["total"][1] += power
                    usage_data[room]["total"][2] += WorstPower

            averages = {room: {
                "energy":usage_data[room]['total'][0] / len(devices),
                "power":usage_data[room]['total'][1] / len(devices),
                "WorstPower":usage_data[room]['total'][2] / len(devices),
                "Grade": assign_grade(usage_data[room]['total'][1] / len(devices), usage_data[room]['total'][2] / len(devices)) *100
            } for room, devices in usage_data.items() if len(devices) > 1}

            return jsonify(averages)

        except Exception as e:
            return jsonify({'error': str(e)})

    return 'Hello, this is the index page!'

@app.route("/usage", methods=['GET'])
def get_usage():
    return jsonify(usage_data)

@app.route("/room/<room_name>/<uuid>", methods=['GET'])
def get_room_info(room_name, uuid):
    if room_name in averages:
        return jsonify({"user": uuid, room_name: averages[room_name]})
    else:
        return jsonify({"error": "Room not found"})

@app.route("/")
def hello_world():
    return "<p>Hello, world!!</p>"

if __name__ == "__main__":
    app.run(debug=True)
