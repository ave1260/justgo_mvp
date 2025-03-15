from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)

# 환경 변수에서 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

# PostgreSQL 설정
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 🚀 여행 테이블 모델 정의
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(20), nullable=False)

# ✅ 앱 시작 시 자동으로 테이블 생성
with app.app_context():
    db.create_all()  # ✅ 여기서 테이블을 생성하도록 변경!

# ✅ 서버 상태 체크 API
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "message": "Server is running"}), 200

# ✅ 여행 목록 조회 API (DB에서 가져오기)
@app.route('/api/trips', methods=['GET'])
def get_trips():
    trips = Trip.query.all()
    trips_list = [{"id": trip.id, "destination": trip.destination, "duration": trip.duration} for trip in trips]
    response_data = json.dumps({"trips": trips_list}, ensure_ascii=False)
    return response_data, 200, {'Content-Type': 'application/json; charset=utf-8'}

# ✅ 여행 추가 API (DB에 저장)
@app.route('/api/trips', methods=['POST'])
def add_trip():
    data = request.json
    if not data or not data.get("destination") or not data.get("duration"):
        return jsonify({"message": "Invalid data"}), 400
    
    new_trip = Trip(destination=data["destination"], duration=data["duration"])
    db.session.add(new_trip)
    db.session.commit()

    response_data = json.dumps({"message": "Trip added", "trip": {"id": new_trip.id, "destination": new_trip.destination, "duration": new_trip.duration}}, ensure_ascii=False)
    return response_data, 201, {'Content-Type': 'application/json; charset=utf-8'}

# ✅ 루트 경로 (Welcome 메시지)
@app.route('/')
def home():
    return jsonify({"message": "Welcome to JustGo API!"}), 200

# ✅ 데이터베이스 연결 테스트 API
@app.route('/dbtest', methods=['GET'])
def db_test():
    try:
        conn = db.engine.connect()
        conn.close()
        return jsonify({"message": "Database Connected!", "status": "OK"}), 200
    except Exception as e:
        return jsonify({"message": "Database Connection Failed", "status": "ERROR", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)





