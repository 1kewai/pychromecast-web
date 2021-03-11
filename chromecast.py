#import処理周り
from flask import send_file,request,Flask
import os
import pychromecast
from gtts import gTTS
import gc
import time

app=Flask(__name__)
finished=0
speaklock=0

#Google Castへオーディオファイルを提供
@app.route("/media")
def send_mp3():
    global finished
    finished=1
    return send_file("data.mp3")

#Google Castデバイスに喋らせる文をTTSして公開し、URLを通知
@app.route("/speak")
def speak():
    global finished
    global speaklock
    #ロックを実行
    if speaklock==1:
        return "Service Unavailable",503
    speaklock=1
    finished=0

    #引数が正しいかチェックを行う
    try:
        print("devicename="+request.args.get("device")+"  "+"sentence="+request.args.get('sentence'))
    except:
        speaklock=0
        return "Bad Request",400

    #実際の処理を行う
    try:
        device=request.args.get("device")
        cast,browser=pychromecast.get_listed_chromecasts(friendly_names=[device])
        mc=cast[0].media_controller
        cast[0].wait()
        tts=gTTS(text=request.args.get('sentence'),lang="ja")
        tts.save("data.mp3")
        if mc.status.player_is_playing:
            speaklock=0
            finished=1
            pychromecast.discovery.stop_discovery(browser)
            return "Service Unavailable",503
        mc.play_media("http://192.168.100.11:10000/media","audio/mp3")
        pychromecast.discovery.stop_discovery(browser)#chromecast discoveryを停止してシステムリソースを節約する
        time.sleep(1)
        #処理が正常終了し、Google castからメディアデータへのアクセスが行われた場合
        if finished==1:
            speaklock=0
            return "OK",200
        #処理は正常終了したが、Google castからのwebサーバーへのアクセスが行われない場合
        if finished==0:
            speaklock=0
            return "Accepted",202
    #Internal Error
    except:
        try:
            pychromecast.discovery.stop_discovery(browser)#chromecast discoveryを停止してシステムリソースを節約する
        except:
            pass
        speaklock=0
        return "Internal Error",500


#一時データの削除
@app.route("/clear")
def clear():
    try:
        os.remove("data.mp3")
    except:
        pass
    print("Cleared temporary data.")
    return "OK",200

#Google Castの情報を取得するためのAPI
@app.route("/info")
def info():
    device=""
    try:
        device=request.args.get("device")
    except:
        return "Bad Request",400
    try:
        cast,browser=pychromecast.get_listed_chromecasts(friendly_names=[device])
        pychromecast.discovery.stop_discovery(browser)
        return str(cast[0]),200
    except:
        pychromecast.discovery.stop_discovery(browser)
        return "Internal Error",500

#Google Castのメディア再生状況を取得するためのAPI
@app.route("/status")
def status():
    device=""
    try:
        device=request.args.get("device")
    except:
        return "Bad Request",400
    try:
        cast,browser=pychromecast.get_listed_chromecasts(friendly_names=[device])
        cast[0].wait()
        time.sleep(1)
        result=cast[0].media_controller.status
        pychromecast.discovery.stop_discovery(browser)
        print(result)
        return str(result),200
    except:
        pychromecast.discovery.stop_discovery(browser)
        return "Internal Error",500

#Google Castのメディアを一時停止
@app.route("/pause")
def pause():
    device=""
    try:
        device=request.args.get("device")
    except:
        return "Bad Request",400
    try:
        cast,browser=pychromecast.get_listed_chromecasts(friendly_names=[device])
        cast[0].wait()
        time.sleep(1)
        result=cast[0].media_controller.pause()
        pychromecast.discovery.stop_discovery(browser)
        print(result)
        return "OK",200
    except:
        pychromecast.discovery.stop_discovery(browser)
        return "Internal Error",500

#再開
@app.route("/resume")
def resume():
    device=""
    try:
        device=request.args.get("device")
    except:
        return "Bad Request",400
    try:
        cast,browser=pychromecast.get_listed_chromecasts(friendly_names=[device])
        cast[0].wait()
        time.sleep(1)
        result=cast[0].media_controller.play()
        pychromecast.discovery.stop_discovery(browser)
        print(result)
        return "OK",200
    except:
        pychromecast.discovery.stop_discovery(browser)
        return "Internal Error",500

#Google CastデバイスにURLからキャスト
@app.route("/cast")
def cast():
    #引数が正しいかチェックを行う
    try:
        print("devicename="+request.args.get("device")+"  URL="+request.args.get("url")+"  metadata="+request.args.get("metadata"))
    except:
        return "Bad Request",400

    #実際の処理を行う
    try:
        device=request.args.get("device")
        cast,browser=pychromecast.get_listed_chromecasts(friendly_names=[device])
        mc=cast[0].media_controller
        cast[0].wait()
        mc.play_media(url,metadata)
        pychromecast.discovery.stop_discovery(browser)#chromecast discoveryを停止してシステムリソースを節約する
        time.sleep(1)
        #処理が正常終了し、Google castからメディアデータへのアクセスが行われた場合
        return "OK",200
    #Internal Error
    except:
        try:
            pychromecast.discovery.stop_discovery(browser)#chromecast discoveryを停止してシステムリソースを節約する
        except:
            pass
        return "Internal Error",500

#ウェブアプリ実行
if __name__ == "__main__":
        app.run(debug=True,host="0.0.0.0",port=10000)
