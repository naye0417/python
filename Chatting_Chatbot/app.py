from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import socket
import json
from rulebase_answer import *
import threading

# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소
port = 5051  # 챗봇 엔진 서버 통신 포트

# Flask 어플리케이션
app = Flask(__name__)
CORS(app)



# 챗봇 엔진 서버와 통신
def get_answer_from_engine(bottype, query):

    if query == "오늘 날씨 알려줘":
        return  trans_json(query, answer_weather())
    elif query == "네이버 기사 알려줘":
        return  trans_json(query, answer_naver_news())
    elif query == "네이버 기사 분석해줘":
        # analysis_naver = threading.Thread(target=answer_analysis_naver)
        # analysis_naver.start()
        wordInfo, ret_data = answer_analysis_naver()
        analysis_showGraph = threading.Thread(target=showGraph, args=(wordInfo, "histogram.png"))
        analysis_showGraph.start()
        analysis_WordCloud = threading.Thread(target=saveWordCloud, args=(wordInfo, "naver_cloud.png"))
        analysis_WordCloud.start()
        return  trans_json(query, ret_data)
    elif query == "네이버 영화 순위 보여줘":
        return  trans_json(query, answer_naver_movie_ranking())
    elif query == "네이버 사이트 보여줘":
        naver_site = threading.Thread(target=answer_naver_site)
        naver_site.start()
        return  trans_json(query, "Hello")
    elif query == "다음 사이트 보여줘":
        daum_site = threading.Thread(target=answer_daum_site)
        daum_site.start()
        return  trans_json(query, "Hello")
    elif query == "넌 누구니?":
        return  trans_json(query, "저는 어따세워 챗봇 '어땃🚘' 입니다")
    elif query == "오늘 날씨 어때?":
        return  trans_json(query, "오늘 날씨 너무 좋아요! 커피한잔 하시는거 어떠세요??")
    elif query == "이 사이트는 어떤 사이트니?":
        return  trans_json(query, " [어따세워]는 주차장 공유 플랫폼 사이트입니다. 한번 이용해 보시겠나요?")
    elif query == "너 너무 귀여운거 아니니?":
        return  trans_json(query, " 헤헤😊 저도 그렇게 생각해요😎")    
    else:
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
            return jsonify(ret)

        elif bot_type == "KAKAO":
            # 카카오톡 스킬 처리
            pass

        elif bot_type == "NAVER":
            # 네이버톡톡 Web hook 처리
            pass
        elif bot_type == "CHAT":
            print("chat client msg");
            return "Thank you"
            pass
        else:
            # 정의되지 않은 bot type인 경우 404 오류
            abort(404)

    except Exception as ex:
        # 오류 발생시 500 오류
        abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
