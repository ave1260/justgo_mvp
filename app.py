from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# 서버 상태 체크 API
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "message": "Server is running"}), 200

# 임시 여행 데이터 (나중에 DB 연동 예정)
trips = [
    {"id": 1, "destination": "서울", "duration": "3일"},
    {"id": 2, "destination": "부산", "duration": "2일"}
]

# 여행 목록 조회 API (한글 깨짐 방지 적용)
@app.route('/api/trips', methods=['GET'])
def get_trips():
    response_data = json.dumps({"trips": trips}, ensure_ascii=False)  # 🔥 한글 유지!
    return response_data, 200, {'Content-Type': 'application/json; charset=utf-8'}

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
    response_data = json.dumps({"message": "Trip added", "trip": new_trip}, ensure_ascii=False)  # 🔥 한글 유지!
    return response_data, 201, {'Content-Type': 'application/json; charset=utf-8'}

# ✅ 루트 경로 추가 (올바른 위치)
@app.route('/')
def home():
    return jsonify({"message": "Welcome to JustGo API!"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)



