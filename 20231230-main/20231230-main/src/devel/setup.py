from setuptools import setup

package_name = 'devel'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='uchida',
    maintainer_email='uchida@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'pub = devel.20231016_pub_test:main',#送信
        'talker = devel.publisher_member_function',#送信
        'sub = devel.sub_face_movie:main',#顔の動画
        'speech = devel.sub_speech:main',
        'chat = devel.voice_chat_bot:main',
        'gpt = devel.sub_gpt:main',#テキストを読み込んでvoicevoxで再生
        'pubvoice = devel.pub_voice_enter:main',
        'pubvoicetest = devel.pub_voice_enter_test:main',
        'motor = devel.sub_motor:main',
        'record_test = devel.record_test:main',#録音？
        'record_pub = devel.record_pub:main',#録音？
        ],
    },
)
