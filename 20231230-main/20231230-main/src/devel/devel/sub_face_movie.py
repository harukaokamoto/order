import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import datetime
from sensor_msgs.msg import Image
import time
import math
from std_msgs.msg import Int32
#from devel import record_pub
#import sys
#from timeout_decorator import timeout, TimeoutError


# Sring型メッセージをサブスクライブして端末に表示するだけの簡単なクラス
class HscrSub(Node):
    def __init__(self):# コンストラクタ
        super().__init__('HSCR_Robot_sub_node')
        # サブスクライバの生成
        #self.sub = self.create_subscription(String,'topic', self.callback, 10)#topicっていう名前の箱のサブスクライブ、Stringは形受け取る
        self.publisher = self.create_publisher(Image,'result',10)#大事！resultっていう名前の箱にパブリッシュしてる。送ってる。rqtは通信を見えるようにする。動画をresultに送ってrqtでみてる。
        self.sub_char_c = self.create_subscription(Int32,'m_result',self.callback,10)

    def movie_start(self,c_msg):#main４４行目の中で動作してるこの中変える28〜39ロスで動画流すルール
        #n = float_var
        #print(n)
        msg=0
        print(type(c_msg))
        print(c_msg.data)
        n = int(c_msg.data)
        print(type(n.data))
        for n in range(n):
            #msg = String()
            #msg = Int32()
            #msg.data = n
            self.sub_char_c.publish(c_msg)
            
            br = CvBridge()
            cap0 =  cv2.VideoCapture(r"/home/uchida/devel1/src/devel/devel/movie/10char1s.mp4")
            while True:
                ret1, frame1 = cap0.read()
                if ret1:               
                    frame1 = cv2.resize(frame1, (1920, 1080))
                    movie1_br =br.cv2_to_imgmsg(frame1,'bgr8')
                    self.publisher.publish(movie1_br)
                    cv2.waitKey(10)
                else:
                    cap0.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    break
            
            print("end")

    def callback(self, c_msg):  # コールバック関数 送られたときに起動
        self.get_logger().info(f'サブスクライブ: {c_msg.data}')
        print(type(c_msg))
        print(c_msg.data)
        n = int(c_msg.data)
        print(n)
        #print(type(n.data))
        for n in range(n):
            #msg = String()
            #msg = Int32()
            #msg.data = n
            
            br = CvBridge()
            cap0 =  cv2.VideoCapture(r"/home/uchida/devel1/src/devel/devel/movie/10char1s.mp4")
            while True:
                ret1, frame1 = cap0.read()
                if ret1:               
                    frame1 = cv2.resize(frame1, (1920, 1080))
                    movie1_br =br.cv2_to_imgmsg(frame1,'bgr8')
                    self.publisher.publish(movie1_br)
                    cv2.waitKey(10)
                else:
                    cap0.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    break
            
            print("end")

        





def main(args=None):  # main¢p
    try:
        rclpy.init()#初期化
        node = HscrSub()#nodeにHscrを代入？
        c_msg=String()#stringは文字列いれれる
        while True:           
            rclpy.spin_once(node)#一回ノードを起動する？
            time.sleep(2)#10秒待つ（喋り始めに合わせる）
            #node.movie_start(c_msg)#movie_startを実行する
    except KeyboardInterrupt:
        pass    #ctl+C(KeyboardInterrupt) node finish

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
