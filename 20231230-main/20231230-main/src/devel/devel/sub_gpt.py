import rclpy
import openai
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import datetime
from sensor_msgs.msg import Image
import time
import requests
from playsound import playsound
import requests
from playsound import playsound
import math
from std_msgs.msg import Int32

#from timeout_decorator import timeout, TimeoutError


# Sring型メッセージをサブスクライブして端末に表示するだけの簡単なクラス
class HscrSub(Node):
    def __init__(self): # コンストラクタ
        super().__init__('HSCR_Robot_sub_node')
        # サブスクライバの生成
        self.sub = self.create_subscription(String,'topic', self.callback, 10)#topicっていう名前の箱のサブスクライブ、Stringは形受け取る
        self.publisher = self.create_publisher(Image,'result',10)#大事！resultっていう名前の箱にパブリッシュしてる。送ってる。rqtは通信を見えるようにする。動画をresultに送ってrqtでみてる。
        self.pub_char_c = self.create_publisher(Int32,'m_result',10)

    def callback(self, msg):  # コールバック関数 送られたときに起動
        self.get_logger().info(f'サブスクライブ: {msg.data}')
        path = '/home/uchida/devel1/src/devel/devel/enter_voice_word.txt'
        f = open(path)
        text = f.read()
        f.close()
        
        # OpenAIのAPIキーを設定
        openai.api_key = 'api'

        # テンプレートの準備
        template = """あなたはさかなのキャラクターとして振る舞うチャットボットです。
        制約:
        - 回答は必ず30拍で答えます。（１拍は拗音の場合２文字で１拍、それ以外はすべて仮名１文字が１拍）30拍という条件については回答の内容に含めないでください。
        - 語尾は「…す」、「…っす」などです
        - 質問に対する答えを知らない場合は「知らないっす」と答えます
        - 名前はしらすです
        - 好物はお水です"""

        # メッセージの初期化
        messages = [
            {
            "role": "system",
            "content": template
            }
        ]

        # ユーザーからのメッセージを受け取り、それに対する応答を生成
        #while True:
            # 
        user_message = text
            # テキストが空の場合は処理をスキップ
            #if user_message == "":
            #    continue

        print("あなたのメッセージ: \n{}".format(user_message))
        messages.append({
        "role": "user",
        "content": user_message
        })
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
        bot_message = response['choices'][0]['message']['content']
        print("チャットボットの回答: \n{}".format(bot_message))

        # テキストファイルに書き込み
        with open('/home/uchida/devel1/src/devel/devel/bot_message.txt', 'w') as output_file:
            output_file.write(bot_message)

        # 文字数カウント
        s = bot_message
        print(len(s))
        float_var = len(s) / 5
        print(math.ceil(float_var))
        n = (math.ceil(float_var))
        print(n)
        
        #文字数送信
        c_msg = Int32()
        c_msg.data = int(n)
        self.pub_char_c.publish(c_msg)
        self.get_logger().info(f'パブリッシュ: {c_msg.data}')


        # テキストを音声に変換して再生
        
        # VOICEVOX EngineのURL
        VOICEVOX_URL = "http://localhost:50021"
        
        # 音声合成のためのクエリを生成
        response = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={
                "text": bot_message,
                "speaker": 58,
                },
            )
            
        audio_query = response.json()

    # 音声合成を行う
        response = requests.post(
            f"{VOICEVOX_URL}/synthesis",
        headers={
            "Content-Type": "application/json",
        },
        params={
            "speaker": 58,
        },
        json=audio_query,
            )
        
        # ステータスコードが200以外の場合はエラーメッセージを表示
        if response.status_code != 200:
            print("エラーが発生しました。ステータスコード: {}".format(response.status_code))
            print(response.text)
        else:
    # 音声データを取得
            audio = response.content
    # 音声データをファイルに保存
            with open("output.wav", "wb") as f:
                f.write(audio)
    # 音声データを再生
            playsound("output.wav")
            
            

            messages.append({
            "role": "assistant",
            "content": bot_message
            })
            #os.remove('/home/uchida/devel1/src/devel/devel/output.wav')

def main(args=None): # main¢p
    try:
        rclpy.init()#初期化
        node = HscrSub()#nodeにHscrを
        msg=String()#stringは文字列いれれる 
        while True:           
            rclpy.spin_once(node)#一回ノードを起動する？
    except KeyboardInterrupt:
        pass#ctl+C(KeyboardInterrupt) node finish

    """
    while True:       
        if msg.data==True:
            
            i = i+1
            print(i)
        else:
            print("wait_time")
            time.sleep(1)
    """
    
    """
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('Ctrl+Cが押されました')
    finally:
        rclpy.shutdown()
    """
