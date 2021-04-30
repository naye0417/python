from flask import Flask, request, jsonify, abort
import socket
import json
import scraping_weather
from flask import Flask
from flask_cors import CORS



# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소
port = 5050  # 챗봇 엔진 서버 통신 포트

# Flask 어플리케이션
app = Flask(__name__)
CORS(app)

# 챗봇 엔진 서버와 통신
def get_answer_from_engine(bottype, query):
    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청
    json_data = {
        'Query': query,
        'BotType': bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()

    return ret_data

def get_answer_from_scraping():
    local, temp , text = scraping_weather.weather()

    data = {
        'local': local,
        'temp': temp,
        'text': text
    }

    ret_data = json.dumps(data)
    return ret_data


@app.route('/', methods=['GET'])
def index():
    print('hello')

# 챗봇 엔진 query 전송 API
@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()

    try:
        if bot_type == 'TEST':
            # 챗봇 API 테스트
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            print("TEST 요청")
            return jsonify(ret)

        elif bot_type == "KAKAO":
            print("KAKAO 요청")
            # 카카오톡 스킬 처리
            pass

        elif bot_type == "NAVER":
            print("NAVER 요청")
            # 네이버톡톡 Web hook 처리
            pass
        elif bot_type == "WEATHER":
            print("WEATHER 요청")
            ret = get_answer_from_scraping()

            return jsonify(ret)

        else:
            # 정의되지 않은 bot type인 경우 404 오류
            abort(404)

    except Exception as ex:
        # 오류 발생시 500 오류
        abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(port=5000)
