#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from base64 import b64decode
try:
    import rapidjson as json
except:
    import json

from pprint import pprint
from requests import post

class KeyMoji:
    def __init__(self, username="", keymojiKey="", url="https://api.droidtown.co/KeyMoji"):
        '''
        username = ""       # 你註冊時的 email。
        keymoji_key = ""    # 您完成付費後取得的 keymoji_key 值。
        '''
        try:
            with open("./account.info", "r") as f:
                userDICT = json.loads(f.read())
            self.username = userDICT["email"]
            self.keymojiKey = userDICT["keymoji_key"]
        except:
            self.username = username
            self.keymojiKey = keymojiKey

        self.url = url
        self.strLenLimit = 6000

    def sense2(self, inputSTR, contextSenitivity=True):
        if len(inputSTR) > self.strLenLimit:
            return {"status": False, "msg": "Your input_str is too long. (over {} characters.)".format(self.strLenLimit)}
        payload = {"username": self.username, "keymoji_key": self.keymojiKey,
                   "input_str": inputSTR, "sense": "sense2", "context_sensitivity": contextSenitivity}
        sense2Result = post("{}/API/".format(self.url), json=payload)
        try:
            resultDICT = sense2Result.json()
            return resultDICT
        except Exception as e:
            return {"status": False, "msg": e}

    def sense8(self, inputSTR):
        if len(inputSTR) > self.strLenLimit:
            return {"status": False, "msg": "Your input_str is too long. (over {} characters.)".format(self.strLenLimit)}
        payload = {"username": self.username, "keymoji_key": self.keymojiKey,
                   "input_str": inputSTR, "sense": "sense8"}
        sense8Result = post("{}/API/".format(self.url), json=payload)
        try:
            resultDICT = sense8Result.json()
            return resultDICT
        except Exception as e:
            return {"status": False, "msg": e}

    def tension(self, inputSTR):
        inputStrLen = len(inputSTR)
        if inputStrLen > self.strLenLimit:
            return {"status": False, "msg": "Your input_str is too long. (over {} characters.)".format(self.strLenLimit)}
        if inputStrLen < 180:
            return {"status": False, "msg": "Your length of input_str must contain at least 180 characters."}
        payload = {"username": self.username, "keymoji_key": self.keymojiKey,
                   "input_str": inputSTR, "sense": "tension"}
        tensionResult = post("{}/API/".format(self.url), json=payload)
        try:
            resultDICT = tensionResult.json()
            return resultDICT
        except Exception as e:
            return {"status": False, "msg": e}

    def keymoji2visual(self, resultDICT, path="."):
        if "sense" not in resultDICT or "results" not in resultDICT:
            return {"status": False, "msg": "Invalid arguments."}
        resultDICT["username"] = self.username
        resultDICT["keymoji_key"] = self.keymojiKey
        visualResult = post("{}/Toolkit/".format(self.url), json=resultDICT)
        if visualResult.status_code == 200:
            try:
                result = visualResult.json()
                #pprint(result)
                file_content = b64decode(result["result"]["base64"])
                with open("{}/{}".format(path, result["result"]["name"]),"wb") as f:
                    f.write(file_content)
                return True
            except Exception as e:
                print(e)
        return False


if __name__ == "__main__":
    keymoji = KeyMoji()

    inputSTR = "不要逃啊，卑鄙的傢伙。鬼殺隊一直在對你們有利的黑夜中戰鬥，我們都是有血有肉之軀的人，受傷之後無法簡單治好，失去的性命也無法挽回⋯⋯大哥沒有輸，他真的到了最後、守護到了最後。是你輸了，大哥才沒有輸！謝謝你，我心中的煉獄大哥。一直以來你在我面前擋住了很多攻擊、一直以來你都沒有放棄要成為更好的自己、一直以來有一個懦弱的我，一直躲在你後面，覺得自己很沒用，但你的任務圓滿結束了，從今天起，你可以好好休息。謝謝你一直以來的照顧，沒有讓在場的任何一個人死去。"
    sense2Result = keymoji.sense2(inputSTR)
    pprint(sense2Result)
    print(keymoji.keymoji2visual(sense2Result))

    #sense8Result = keymoji.sense8(inputSTR)
    #pprint(sense8Result)
    #keymoji.keymoji2visual(sense8Result)

    #tensionResult = keymoji.tension(inputSTR)
    #pprint(tensionResult)
    #keymoji.keymoji2visual(tensionResult)


