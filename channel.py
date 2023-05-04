# 변수 = 노션 채널 고유 id
EVENT = "C052BV4T5RN"
BACKEND_EVENT = "C03N40QEDQU"
CLIENT_EVENT = "C040Q0N033J"
DESIGN_EVENT = "C02T71RE9B9"
FRONTED_EVENT = "C046KT6K2NB"
ML_EVENT = "C04FBG664J2"
TEST = "C03P45HG7B9"

# # WS
# EVENT = "C051QNA9AG3"
# BACKEND_EVENT = "C052EGG4J0G"
# CLIENT_EVENT = "C051QRWRD7U"
# DESIGN_EVENT = "C051J84NN22"
# FRONTED_EVENT = "C052EGRCN80"
# ML_EVENT = "C051QN81C2X"
# # TEST = "C03P45HG7B9"
CHANNELS = {
    "channels": [
        #  왼쪽은 노션 Event Type : 오른쪽은 그냥 변수
        {
            # event 채널
            "Academic": EVENT,
            "Bi-Weekly Review": EVENT,
            "Keynote": EVENT,
            "Management": EVENT,
            "Offline Event": EVENT,
            "Online Event": EVENT,
        },
        {
            # position별 채널
            "Backend Event": BACKEND_EVENT,
            "Client Event": CLIENT_EVENT,
            "Design Event": DESIGN_EVENT,
            "Frontend Event": FRONTED_EVENT,
            "ML Event": ML_EVENT,
            "bot-lab": TEST,
        },
        {EVENT},  # 아무 멘션 없을 시 EVENT 채널에
    ]
}
