import requests
data = {
    "Kitchen": {
        "Microwave": ["08:00", "08:30"],
        "Oven": ["20:00", "20:15"],
        "Fans": ["11:00", "14:30"],
        "Lampe": ["08:00", "08:30"],
        "Lampe": ["20:00", "23:00"],


    },
    "Garage": {
        "Car": ["00:00", "08:00"],
        "Lampe": ["08:00", "08:30"],
        "Lampe": ["20:00", "23:59"],
    },
    "LivingRoom": {
        "Lampe": ["07:00", "23:00"],
        "TV": ["12:00", "15:00"],
        "PlayStation": ["12:00", "15:00"]
    },
    "BedRoom": {
        "Lampe": ["12:00", "23:30"],
        "Lampe": ["12:00", "23:30"],
        "Lampe": ["12:00", "23:30"],
        "Lampe": ["12:00", "23:30"],
        "Lampe": ["12:00", "23:30"]
    }
}

res = requests.post('http://localhost:5000/api/power', json=data)
if res.ok:
    print(res.json())
