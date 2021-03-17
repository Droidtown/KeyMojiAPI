# KeyMoji [Emotions in Formula]

KeyMoji 關鍵情緒偵測 (**SENSE2、SENSE8、Tension**) 採用不同於其它「素人標記」和「純機器學習」的文本情緒偵測分析工具，結合了「**句型**」、「**邏輯語意**」和「**詞彙模型**」，設計出一個完整的「情緒計算過程」。

[完整介紹](https://api.droidtown.co/document/#KeyMoji)

## 安裝方法

```sh
pip3 install KeyMoji
```

## 使用方法
[KeyMoji Website Demo](https://api.droidtown.co/#keymoji)  
[KeyMojiAPI Documentation](https://api.droidtown.co/KeyMoji/document/)

### SENSE2
```python
from KeyMojiAPI import KeyMoji
keymoji = KeyMoji(username="your_username@mail.com", keymojiKey="your_keymoji_key")

inputSTR = "他逃離了危險的災難"
result = keymoji.sense2(inputSTR)
print(result)
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

![sense2](https://www.droidtown.co/static/public_img/sense2.png)

### SENSE8
```python
from KeyMojiAPI import KeyMoji
keymoji = KeyMoji(username="your_username@mail.com", keymojiKey="your_keymoji_key")

inputSTR = "他逃離了危險的災難"
result = keymoji.sense8(inputSTR)
print(result)
```

```json
{
    "status": true,
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