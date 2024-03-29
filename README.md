# KeyMoji [Emotions in Formula]

KeyMoji 關鍵情緒偵測 (**SENSE2、SENSE8、Tension**) 採用不同於其它「素人標記」和「純機器學習」的文本情緒偵測分析工具，結合了「**句型**」、「**邏輯語意**」和「**詞彙模型**」，設計出一個完整的「情緒計算過程」。

[完整介紹](https://api.droidtown.co/document/#KeyMoji)

## 安裝方法

```sh
pip3 install KeyMojiAPI
```
or
```sh
python3 -m pip install KeyMojiAPI
```

## 使用方法
[KeyMoji Website Demo](https://api.droidtown.co/#keymoji)  
[KeyMojiAPI Documentation](https://api.droidtown.co/KeyMojiAPI/document/)

### SENSE2
```python
from KeyMojiAPI import KeyMoji
# 若您是使用 Docker 版本，無須填入 username, keymoji_key 參數
keymoji = KeyMoji(username="", keymojiKey="")

inputSTR = "他逃離了危險的災難"
# Sense2
sense2Result = keymoji.sense2(inputSTR, model="general", userDefinedDICT={"positive":[], "negative":[], "cursing":[]})
print(sense2Result)
# Sense2 Visualization
status = keymoji.keymoji2visual(sense2Result, filename="kimetsu.png")
```

```json
{
    "status": true,
    "msg": "Success!",
    "results": [
        {
            "score": 0.2798,
            "sentiment": "positive",
            "input_str": "他逃離了危險的災難",
            "cursing": false
        }
    ],
    "sense": "sense2",
    "version": "v101"
}
```

### Visualization

![sense2](https://www.droidtown.co/static/public_img/sense2.png?raw=true)

### SENSE8
```python
from KeyMojiAPI import KeyMoji
# 若您是使用 Docker 版本，無須填入 username, keymoji_key 參數
keymoji = KeyMoji(username="", keymojiKey="")

inputSTR = "他逃離了危險的災難"
sense8Result = keymoji.sense8(inputSTR, model="general", userDefinedDICT={"positive":[], "negative":[], "cursing":[]})
print(sense8Result)
# Sense8 Visualization
status = keymoji.keymoji2visual(sense8Result, filename="kimetsu.zip")
```

```json
{
    "status": True,
    "msg": "Success!",
    "results": [
        {
            "input_str": "他逃離了危險的災難",
            "Joy": 3.7486,
            "Trust": 5.1776,
            "Surprise": 6.7238,
            "Anticipation": 0.9618,
            "Fear": 0.9505,
            "Sadness": 0.9108,
            "Anger": 0.9516,
            "Disgust": 0.8876
        }
    ],
    "sense": "sense8",
    "version": "v101"
}
```

### Visualization

![sense8](https://www.droidtown.co/static/public_img/sense8.png)


### Tension Visualization

![tension](https://www.droidtown.co/static/public_img/tension.png)
