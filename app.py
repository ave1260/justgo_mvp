from flask import Flask, jsonify, request

app = Flask(__name__)

# 서버 상태 체크 API
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "message": "Server is running"}), 200

# 여행 목록 데이터
trips = [
    {"id": 1, "destination": "서울", "duration": "3일"},
    {"id": 2, "destination": "부산", "duration": "2일"}
]

# 여행 목록 조회 API (ensure_ascii=False 적용)
@app.route('/api/trips', methods=['GET'])
def get_trips():
    return jsonify({"trips": trips}), 200, {'Content-Type': 'application/json; charset=utf-8'}

# 여행 추가 API
@app.route('/api/trips', methods=['POST'])
def add_trip():
    data = request.json
    new_trip = {
        "id": len(trips) + 1,
        "destination": data.get("destination"),
        "duration": data.get("duration")
    }
    trips.append(new_trip)
    return jsonify({"message": "Trip added", "trip": new_trip}), 201, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


