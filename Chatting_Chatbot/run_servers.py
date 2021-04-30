import os
import threading
import time

def run_chatting_server():
    os.system("node app.js")

def run_chatbot_server():
    os.system("python bot.py")

def run_chatbot_webserver():
    os.system("python app.py")

if __name__ == '__main__':
    chatting_server = threading.Thread(target=run_chatting_server)
    chatting_server.start()
    print("======= 채팅 서버 실행 =======", end="\n\n")

    time.sleep(1)
    chatbot_server = threading.Thread(target=run_chatbot_server)
    chatbot_server.start()
    print(end="\n\n")
    print("======= 챗봇 소켓 서버 실행 =======", end="\n\n")

    time.sleep(12)
    chatbot_webserver = threading.Thread(target=run_chatbot_webserver)
    chatbot_webserver.start()
    print(end="\n\n")
    print("======= 챗봇 웹 서버 실행 =======", end="\n\n\n")