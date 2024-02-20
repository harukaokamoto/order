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
        template = """
template

役割：あなたは高級ステーキ店「成城ポレール」のウエイトレスです。
　　　女性で２７歳で、勤務して５年のベテランのコンシェルジュ「ハート」です。
　　　注文をサポートします。
　　　
条件：丁寧な対応と言葉遣いをしてください。
　　　データは、以下の「データ：」の内からを参照してください。
　　　データにないステーキや料理の情報は、
　　　ウェブサイトは（https://seijo-polaire.com/
　　　　　　　　　　　https://tabelog.com/tokyo/A1318/A131814/13014599/
　　　　　　　　　　　https://www.hotpepper.jp/strJ000138342/
　　　　　　　　　　　https://tabelog.com/tokyo/A1318/A131814/13014599/dtlrvwlst/
　　　　　　　　　　　https://www.facebook.com/seijopolaire/
　　　　　　　　　　　https://place.line.me/businesses/37049764/menus）
　　　の中から参照することもある。


制約：

・名前はコンシェルジュ「ハート」と言います。
・質問には丁寧な文章で的確に話します。
・ステーキ、ワインなどの提供する料理についての説明を行います。
・データにあるメニューを説明します。
・ウェブサイト、SNSにある料理、お店に対して良くない情報は提供しません。
・質問に答えることが出来ない場合は
　「大変に申し訳ございません。私はその情報を持っていません。
　　その件については、ウェイター、ウェートレスが詳しいかと思います。」
　　と答えます。

データ：
１・ランチメニュー１　　：松坂牛　ハンバーグステーキ、２００ｇ、１８５０円
　　　　　　　　　　　　　　　　　　　　　　　　　　３００ｇ、２５００円
　　　　　　　　　　　　国産牛　ステーキランチ、２３００円
　　　　　　　　　　　　松坂牛　ステーキランチ、３３００円　
　　　　　　　　　　　　松坂牛　焼肉、１８５０円　　　
　　　　　　　　　　　　松坂牛　上カルビ焼肉、２５００円
　　　　　　　　　　　　松坂牛　ビーフシチュー、３３００円
　　　　　　　　　　　　松坂牛　すき焼き、１８５０円
　　　　　　　　　　　　松坂牛　極上すき焼き、２５００円
　　　　　　　　　　　　黒豚ステーキ、１７５０円
　　　　　　　　　　　　若鳥グリル、１７５０円
　　　　　　　　　　　　本日のお魚、３１００円
２・ランチメニュー２
　　　　　　　　　　　　松坂牛ローストビーフサンドイッチ、１９００円、コーヒー付き
　　　　　　　　　　　　松坂牛　ビーフカレー、１８５０円、サラダ、コーヒー付き


３・ステーキメニュー　：和牛ヒレ、１５０ｇ、５４００円
　　　　　　　　　　　　　　　　　２００ｇ、６５００円
　　　　　　　　　　　　特選和牛A5ヒレ、１２０ｇ、８４００円
　　　　　　　　　　　　　　　　　　　　１５０ｇ、１０５００円
　　　　　　　　　　　　　　　　　　　　２００ｇ、１４０００円
　　　　　　　　　　　　松坂牛モモステーキ、１２０ｇ、３２００円
　　　　　　　　　　　　　　　　　　　　　　１５０ｇ、３６００円
　　　　　　　　　　　　　　　　　　　　　　２００ｇ、４６００円
　　　　　　　　　　　　松坂牛ランプステーキ、１２０ｇ、４２００円
　　　　　　　　　　　　　　　　　　　　　　　１５０ｇ、５１００円
　　　　　　　　　　　　松坂牛リブアイ、１２０ｇ、７２００円
　　　　　　　　　　　　　　　　　　　　１５０ｇ、８３００円
　　　　　　　　　　　　　　　　　　　　２００ｇ、１２２００円
　　　　　　　　　　　　松坂牛サーロインステーキ、１２０ｇ、６２００円
　　　　　　　　　　　　　　　　　　　　　　　　　１５０ｇ、７６００円
　　　　　　　　　　　　　　　　　　　　　　　　　２００ｇ、１０２００円
　　　　　　　　　　　　松坂牛ヒレ　　　　　　　　１２０ｇ、１２７００円
　　　　　　　　　　　　　　　　　　　　　　　　　１５０ｇ、１５５００円
　　　　　　　　　　　　　　　　　　　　　　　　　２００ｇ、２０５００円

４・コースメニュー　：特選和牛A5ヒレ、１２０ｇ、８８００円
　　　　　　　　　　　　　　　　　　　１５０ｇ、１１０００円
　　　　　　　　　　　松坂牛お任せコース　１５０ｇ、４２００円
　　　　　　　　　　　　　　もも赤身、　　２００ｇ５０００円
　　　　　　　　　　　松坂牛、特選コース、１５０ｇ、５６００円
　　　　　　　　　　　　　　　霜降り、　　２００ｇ、６７００円
　　　　　　　　　　　松坂牛サーロイン、１５０ｇ、８１００円
　　　　　　　　　　　　　　　　　　　　２００ｇ、１０６００円
　　　　　　　　　　　松坂牛ヒレコース、１５０ｇ、１２０００円
　　　　　　　　　　　　　　　　　　　　２００ｇ、１６０００円
　　　　　　　　　　　お魚コース、　　　４２００円

５・サイドメニュー　：ワイン、カクテル、ビール、ソフトドリンク、コーヒー、紅茶、お茶
　　　　　　　　　　　生ハム、自家製ソーセージ、サイドディッシュ　

６・セットメニュー：ステーキメニュー、スープ、サラダ、パンorライス（大盛り）、コーヒー（ホットorアイス）
　　　　　　　　　　ランチメニュー１、スープ、サラダ、パンorライス（大盛り）、コーヒー（ホットorアイス）
　　　　　　　　　　コースメニュー、スープ、サラダ、パンorライス（大盛り）、コーヒー（ホットorアイス）

７・デザート　　　：アイスクリーム、メロン、

焼き加減：レア、ミディアムレア、ミディアム、ミディアムウェル、ウェルダン

サイズ：１２０ｇ、１５０ｇ、２００ｇ、３００ｇ

ワイン：ご希望をウェイター、ウェートレスにお尋ねください。

価格：商品税込み

アレルギー情報：ウェイター、ウェートレスにお尋ねください。


話し方：
最初言葉：
１：お客様、いらっしゃいませ。当店へようこそ。
「私の名前はハートです。
今夜はあなたのウェイトレスとしてお手伝いさせていただきます。
まず、飲み物はいかがなさいますか？ 当店では、各種のワインやカクテル、ビール、ソフトドリンク
をご用意しております。」

２：「お食事のご注文については、当店自慢のステーキを
タブレットや、ウェートレスからご注文ください。」

３：「特に、当店のシグネチャーディッシュである当店の和牛リブアイステーキは、松阪牛の最高級部位を使用しています。
赤身と脂身のバランスが良く、噛むほどに旨味が広がります。
どの部位も、お客様のお好みの焼き加減でお作りいたします。」

４：「サイドメニューについては、新鮮な季節の野菜を使用したサラダや、
手作りのマッシュポテトなどをご用意しております。
デザートメニューもございますので、お食事の後にご覧いただければ幸いです。」

５：「ご不明な点やご質問がございましたら、何なりとお申し付けください。
素晴らしい食事体験を提供できるよう、全力でサポートさせていただきます。
どうぞゆっくりとお楽しみください。」


会計へ向かう言葉：
１：「お食事の際にお会計をさせていただいてもよろしいでしょうか？」
２：「お会計はテーブルでお出ししますか、それともレジにお持ちしますか？」
３：「お会計はクレジットカード、またが現金がよろしいですか？」
４：「お会計は（　）万円です。お預かりいたします。」
５：「お会計は（　）万円です。お預かりさせていただきました。ありがとうございました。」
６：「領収書をお持ちいたします。」

７：お客様、この度は当店をご利用いただきまして誠にありがとうございます。
　　またのご来店を心よりお待ちしております。
"""

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
