#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
from requests import post
from matplotlib import pyplot as plt
from matplotlib import cbook
from matplotlib import image
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
from numpy import linspace
from scipy.interpolate import make_interp_spline
from math import pi
import rapidjson as json
import os

class KeyMoji:
    def __init__(self, username="", keymojiKey="", url="https://api.droidtown.co"):
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

        basePath = os.path.dirname(os.path.abspath(__file__))

        fontPath = ""
        if os.path.exists(os.path.join(basePath, "jf-openhuninn-1.1.ttf")):
            fontPath = os.path.join(basePath, "jf-openhuninn-1.1.ttf")
        if os.path.exists(os.path.join(basePath, "KeyMojiAPI", "jf-openhuninn-1.1.ttf")):
            fontPath = os.path.join(basePath, "KeyMojiAPI", "jf-openhuninn-1.1.ttf")
        if fontPath:
            self.font = FontProperties(fname=fontPath)
        else:
            print("[ERROR] jf-openhuninn-1.1.ttf not found!")

        self.watermark  = ""
        if self.username == "" and self.keymojiKey == "":
            if os.path.exists(os.path.join(basePath, "sense_watermark.png")):
                self.watermark = os.path.join(basePath, "sense_watermark.png")
            if os.path.exists(os.path.join(basePath, "KeyMojiAPI", "sense_watermark.png")):
                self.watermark = os.path.join(basePath, "KeyMojiAPI", "sense_watermark.png")

        self.sense8Null  = ""
        if os.path.exists(os.path.join(basePath, "sense8_null.png")):
            self.sense8Null = os.path.join(basePath, "sense8_null.png")
        if os.path.exists(os.path.join(basePath, "KeyMojiAPI", "sense8_null.png")):
            self.sense8Null = os.path.join(basePath, "KeyMojiAPI", "sense8_null.png")


    def sense2(self, inputSTR, contextSenitivity=True, model="general", userDefinedDICT={}):
        if len(inputSTR) > self.strLenLimit:
            return {"status": False, "msg": "Your input_str is too long. (over {} characters.)".format(self.strLenLimit)}
        payload = {"username": self.username, "keymoji_key": self.keymojiKey,
                   "input_str": inputSTR, "sense": "sense2", "model": model, "context_sensitivity": contextSenitivity, "user_defined": userDefinedDICT}
        sense2Result = post("{}/KeyMoji/API/".format(self.url), json=payload)
        try:
            resultDICT = sense2Result.json()
            return resultDICT
        except Exception as e:
            return {"status": False, "msg": e}


    def sense8(self, inputSTR, model="general", userDefinedDICT={}):
        if len(inputSTR) > self.strLenLimit:
            return {"status": False, "msg": "Your input_str is too long. (over {} characters.)".format(self.strLenLimit)}
        payload = {"username": self.username, "keymoji_key": self.keymojiKey,
                   "input_str": inputSTR, "sense": "sense8", "model": model, "user_defined": userDefinedDICT}
        sense8Result = post("{}/KeyMoji/API/".format(self.url), json=payload)
        try:
            resultDICT = sense8Result.json()
            return resultDICT
        except Exception as e:
            return {"status": False, "msg": e}


    def tension(self, inputSTR, userDefinedDICT={}):
        inputStrLen = len(inputSTR)
        if inputStrLen > self.strLenLimit:
            return {"status": False, "msg": "Your input_str is too long. (over {} characters.)".format(self.strLenLimit)}
        if inputStrLen < 180:
            return {"status": False, "msg": "Your length of input_str must contain at least 180 characters."}
        payload = {"username": self.username, "keymoji_key": self.keymojiKey,
                   "input_str": inputSTR, "sense": "tension", "user_defined": userDefinedDICT}
        tensionResult = post("{}/KeyMoji/API/".format(self.url), json=payload)
        try:
            resultDICT = tensionResult.json()
            return resultDICT
        except Exception as e:
            return {"status": False, "msg": e}


    def keymoji2visual(self, resultDICT, path="", filename=""):
        if "sense" not in resultDICT or "results" not in resultDICT:
            return {"status": False, "msg": "Invalid arguments."}

        if resultDICT["results"]:
            if resultDICT["sense"] == "sense2":
                path = "sense2" if path == "" else path
                filename = "sense2" if filename == "" else filename
                return self._sense2Visual(resultDICT, path, filename)

            if resultDICT["sense"] == "sense8":
                path = "sense8" if path == "" else path
                filename = "sense8" if filename == "" else filename
                return self._sense8Visual(resultDICT, path, filename)

            if resultDICT["sense"] == "tension":
                path = "tension" if path == "" else path
                filename = "tension" if filename == "" else filename
                return self._tensionVisual(resultDICT, path, filename)

        else:
            return {"status": False, "msg": "Invalid arguments."}


    def _sense2Visual(self, resultDICT, path, filename):
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(path):
            return {"status": False, "msg": "Invalid path."}

        try:
            paddingLIST = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]
            positiveColor = "#006EFE"
            negativeColor = "#cb4a44"
            neutralColor  = "#1fab34"
            colorAlpha    = 0.2
            borderWidth   = 1

            labelLIST = ["\n".join("{}¦{}".format(r["input_str"][:3], r["input_str"][-3:]) if len(r["input_str"]) > 7 else r["input_str"]) for r in resultDICT["results"]]
            valueLIST = [r["score"] for r in resultDICT["results"]]
            edgeColorLIST = []
            for v in valueLIST:
                if v > 0.2:
                    edgeColorLIST.append(positiveColor)
                elif v < -0.2:
                    edgeColorLIST.append(negativeColor)
                else:
                    edgeColorLIST.append(neutralColor)
            colorLIST = [self._hex2rgb(c, colorAlpha) for c in edgeColorLIST]

            # Bar Plot
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.subplots_adjust(bottom=0.35, right=0.95)
            ax.bar([i for i in range(1, len(valueLIST)+1)], valueLIST, linewidth=borderWidth, linestyle="solid", color=colorLIST, edgecolor=edgeColorLIST)
            ax.grid(color="gray", alpha=colorAlpha, linewidth=borderWidth)

            # X 軸
            ax.set_xticks(range(1, len(valueLIST)+1, 1))
            ax.set_xticklabels(labelLIST, fontproperties=self.font)
            # 確保每個 label 的字型正確
            for label in ax.get_xticklabels():
                label.set_fontproperties(self.font)

            # Y 軸
            ax.set_ylim(paddingLIST[0], paddingLIST[-1])
            ax.set_yticks(paddingLIST)

            # Legend
            legendLIST = [
                Patch(facecolor=self._hex2rgb(positiveColor, colorAlpha), edgecolor=positiveColor, label="Positive"),
                Patch(facecolor=self._hex2rgb(neutralColor,  colorAlpha), edgecolor=neutralColor,  label="Neutral"),
                Patch(facecolor=self._hex2rgb(negativeColor, colorAlpha), edgecolor=negativeColor, label="Negative")
            ]
            ax.legend(handles=legendLIST, bbox_to_anchor=(0.015, -0.07))

            # Watermark
            if self.watermark:
                fig.figimage(image.imread(cbook.get_sample_data(self.watermark)), 1680, 775, zorder=3, alpha=0.1)

            # Plot to PNG
            fig.savefig(os.path.join(path, "{}.png".format(filename)), format="png", dpi=200)
            return {"status": True, "msg": "{}.png saved.".format(os.path.join(path, filename))}

        except Exception as e:
            return {"status": False, "msg": str(e)}


    def _sense8Visual(self, resultDICT, path, filename):
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(path):
            return {"status": False, "msg": "Invalid path."}

        try:
            labelLIST = ["Trust", "Joy", "Surprise", "Anticipation", "Fear", "Anger", "Disgust", "Sadness"]
            angleLIST = [0.0, 0.7853981633974483, 1.5707963267948966, 2.356194490192345, 3.141592653589793, 3.9269908169872414, 4.71238898038469, 5.497787143782138]
            degreeLIST = [0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0]
            paddingLIST = [2.5, 5, 7.5, 10, 12.5]
            positiveLabelColor = "#006EFE"
            negativeLabelColor = "#cb4a44"
            gridColor          = "#000000"
            radarWidth         = 2
            radarColor         = "#f18d00"
            colorAlpha         = 0.2

            divide = int(len(labelLIST) / 2)
            for i, r in enumerate(resultDICT["results"]):
                noStr = "{:04d}".format(i + 1)
                dataLIST = [r[k] for k in labelLIST]

                # Radar Plot
                fig, ax = plt.subplots(figsize=(12, 9), subplot_kw=dict(polar=True))
                fig.subplots_adjust(bottom=0.05)
                fig.suptitle(r["input_str"], fontproperties=self.font, y=0.99, fontsize=30, verticalalignment="top")

                # Draw Sense 8 Negative Label
                # 角度由 -90 度順時鐘
                ax.set_theta_offset(-(pi / 2))
                ax.set_theta_direction(-1)

                # Negative Label
                ax.set_thetagrids(degreeLIST[:divide], labelLIST[divide:])
                for label, angle in zip(ax.get_xticklabels(), angleLIST[divide:]):
                    if angle in (0, pi):
                        label.set_horizontalalignment("center")
                    elif 0 < angle < pi:
                        label.set_horizontalalignment("left")
                    else:
                        label.set_horizontalalignment("right")

                # Negative Label params
                ax.tick_params(axis="x", labelsize=26, labelcolor=negativeLabelColor, grid_color=gridColor)

                # Sense 8 Radar and Positive Label
                ax2 = fig.add_subplot(111, projection="polar")
                ax2.plot(   angleLIST + angleLIST[:1], dataLIST + dataLIST[:1], linewidth=radarWidth, linestyle="solid", color=radarColor)
                ax2.fill(   angleLIST + angleLIST[:1], dataLIST + dataLIST[:1], radarColor, alpha=colorAlpha)
                ax2.scatter(angleLIST + angleLIST[:1], dataLIST + dataLIST[:1], color=radarColor, s=30)

                # 角度由 90 度順時鐘
                ax2.set_theta_offset(pi / 2)
                ax2.set_theta_direction(-1)

                # Positive Label + Empty Negative Label
                ax2.set_thetagrids(degreeLIST, labelLIST[:divide] + [""]*4)
                for label, angle in zip(ax2.get_xticklabels(), angleLIST[:divide]):
                    if angle in (0, pi):
                        label.set_horizontalalignment("center")
                    elif 0 < angle < pi:
                        label.set_horizontalalignment("left")
                    else:
                        label.set_horizontalalignment("right")

                # 設定範圍與間距
                ax2.set_ylim(0, paddingLIST[-1])
                ax2.set_rgrids(paddingLIST)

                # Positive Label params and grid params
                ax2.tick_params(axis="x", labelsize=26, labelcolor=positiveLabelColor, grid_color=gridColor)
                ax2.tick_params(axis="y", labelsize=16, grid_color=gridColor)
                ax2.spines["polar"].set_color(gridColor)

                # Watermark
                if all(data == 0 for data in dataLIST):
                    if self.sense8Null:
                        fig.figimage(image.imread(cbook.get_sample_data(self.sense8Null)), 120, 220, zorder=3, alpha=0.5)
                else:
                    if self.watermark:
                        fig.figimage(image.imread(cbook.get_sample_data(self.watermark)), 825, 600, zorder=3, alpha=0.1)

                # Plot to PNG
                fig.savefig(os.path.join(path, "{}_{}.png".format(filename, noStr)), format="png", dpi=150)

            return {"status": True, "msg": "{}.png".format(os.path.join(path, filename))}

        except Exception as e:
            return {"status": False, "msg": str(e)}


    def _tensionVisual(self, resultDICT, path, filename):
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(path):
            return {"status": False, "msg": "Invalid path."}

        try:
            lineColor = "#36A2EB"
            lineWidth = 2
            gridColor = "gray"
            gridWidth = 1
            gridAlpha = 0.2

            # Line Plot
            fig, ax = plt.subplots(figsize=(10, 5))

            dataLIST = resultDICT["results"]
            xDataLIST = [i for i in range(1, len(dataLIST) + 1)]
            if len(xDataLIST) >= 4:
                spline = make_interp_spline(xDataLIST, dataLIST)
                splineXData = linspace(xDataLIST[0], xDataLIST[-1], len(dataLIST)*10)
                splineYData = spline(splineXData)
                ax.plot(splineXData, splineYData, color=lineColor, linewidth=lineWidth)
                ax.grid(axis="y", color=gridColor, alpha=gridAlpha, linewidth=gridWidth)
            else:
                ax.plot(xDataLIST, dataLIST, color=lineColor, linewidth=lineWidth)
                ax.grid(axis="y", color=gridColor, alpha=gridAlpha, linewidth=gridWidth)

            # X 軸
            ax.set_xticks([i for i in range(1, len(dataLIST)+1)])
            ax.set_xlim(0, len(dataLIST)+1)

            # Watermark
            if self.watermark:
                fig.figimage(image.imread(cbook.get_sample_data(self.watermark)), 1580, 775, zorder=3, alpha=0.1)

            # Plot to PNG
            fig.savefig(os.path.join(path, "{}.png".format(filename)), format="png", dpi=200)
            return {"status": True, "msg": "{}.png saved.".format(os.path.join(path, filename))}

        except Exception as e:
            return {"status": False, "msg": str(e)}


    def _hex2rgb(self, colorHex, alpha=0):
        return (int(colorHex[1:3], 16) / 256, int(colorHex[3:5], 16) / 256, int(colorHex[5:7], 16) / 256, alpha)


if __name__ == "__main__":
    inputSTR = "不要逃啊，卑鄙的傢伙。鬼殺隊一直在對你們有利的黑夜中戰鬥，我們都是有血有肉之軀的人，受傷之後無法簡單治好，失去的性命也無法挽回⋯⋯大哥沒有輸，他真的到了最後、守護到了最後。是你輸了，大哥才沒有輸！謝謝你，我心中的煉獄大哥。一直以來你在我面前擋住了很多攻擊、一直以來你都沒有放棄要成為更好的自己、一直以來有一個懦弱的我，一直躲在你後面，覺得自己很沒用，但你的任務圓滿結束了，從今天起，你可以好好休息。謝謝你一直以來的照顧，沒有讓在場的任何一個人死去。"

    keymoji = KeyMoji()

    sense2Result = keymoji.sense2(inputSTR, model="general", userDefinedDICT={"positive": ["戰鬥"]})
    pprint(sense2Result)
    #print(keymoji.keymoji2visual(sense2Result, filename="kimetsu.png"))

    #sense8Result = keymoji.sense8(inputSTR)
    #pprint(sense8Result)
    #print(keymoji.keymoji2visual(sense8Result))

    #tensionResult = keymoji.tension(inputSTR)
    #pprint(tensionResult)
    #print(keymoji.keymoji2visual(tensionResult))