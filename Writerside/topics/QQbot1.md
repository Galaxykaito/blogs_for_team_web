---
title: QQbot
id: f2982b11-0c7d-4501-af58-c44f598ca6b7
date: 2025-03-31 00:13:07
auther: tachyon
cover: 
excerpt: QQBot 首先安装机器人框架Napcat，然后按照文档进行配置，即可运行QQ机器人。我们要通过 这个东西来实现qq消息和nonebot的消息互通。💕💕💕 原理： napcat会监听qq消息，然后将消息转发给nonebot nonebot根据收到的消息触发功能插件， 插件将生成的内容发送到qq
permalink: /archives/wei-ming-ming-wen-zhang
categories:
tags: 
---

## QQBot
<font color=DeepPink>首先安装机器人框架Napcat，然后按照文档进行配置，即可运行QQ机器人。我们要通过
这个东西来实现qq消息和nonebot的消息互通。</font>💕💕💕


<mark>原理：</mark>
<font color=DarkViolet>
1. napcat会监听qq消息，然后将消息转发给nonebot
2. nonebot根据收到的消息触发功能插件，
3. 插件将生成的内容发送到qq中。</font>

废话不多说，直接上代码。
### 第一步：安装Napcat!
自己去官网根据自己的系统下载对应版本的安装包，然后安装即可。
我用的是windows无头版。官网指路[Napcat](https://napneko.github.io/guide/napcat)。

### 第二步：配置Napcat
<mark>笔者这里没有图床（不想花那点米），就不上图片指引了，</mark>安装好后在文件夹中找到`napcat.bat`文件,双击直接运行。这时候就会让你登录，在跳出来的终端
中你可以看到weibu的地址，类似于`http://127.0.0.1:xxxxx`。`ctrl+鼠标左键`点击这个地址，打开浏览器，然后根据指引登录QQ即可进入控制面板。

然后，网络配置的位置创建的一个反向代理websocket服务器，下面是注意事项：
<font color=HotPink>
* 名称爱咋填咋填.
* url:`ws://（你的qqbot运行的地址，也就是后面提到的bot.py运行的端口）/onebot/v11/ws`
* Token:随便填，但是要和bot.py中的配置一致(详情见bot.py部分的介绍)
其他保持默认即可，根据寻求者的需要进行修改。</font>
### 第三步：机器人程序
直接上代码：

#### 主程序bot.py：
```python
from nonebot import init, get_driver, load_plugin
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
import sys
import os
# 将 PaddleSpeech 的路径添加到 sys.path
paddlespeech_path = os.path.join(os.path.dirname(__file__), "PaddleSpeech")
sys.path.append(paddlespeech_path)
# 初始化 NoneBot
init()

# 获取全局驱动
driver = get_driver()
# 加载单个插件
load_plugin("plugin.demulan")
#load_plugin("plugin.chat_demulan")
#load_plugin("plugin.tts")  # 加载语音合成插件
load_plugin("plugin.tts2")  # 加载新的语音合成插件
load_plugin("plugin.chat_tts")  # 加载新的语音合成插件


# 注册适配器
driver.register_adapter(OneBotV11Adapter)

if __name__ == "__main__":
    # 启动 NoneBot
    driver.run()
<font color=HotPink>
```
简单介绍一下：
1. 首先导入了一些必要的库，包括sys和os，用于处理文件路径和系统相关操作。
2. 然后，将 PaddleSpeech 的路径添加到 sys.path 中，以便在运行时能够正确导入 PaddleSpeech 模块。（tts插件需要用到）
3. 接着，初始化了 NoneBot，并获取![tlsy.png](/upload/tlsy.png)
了全局驱动对象。
4. 然后，加载了几个插件（功能介绍见插件部分）
5. 最后，注册了 OneBotV11Adapter 适配器，并启动了 NoneBot。
</font>

#### 插件部分：
1. demulan.py：
```python
from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.rule import keyword
import os
import base64

# 定义关键词和对应的语音文件
keywords = {
    "迟疑": "夹枪巡逻不要让我听到迟疑的声音.mp3",
    "猛攻": "夹枪巡逻不要让我听到迟疑的声音.mp3",
}

# 创建消息处理器
demulan = on_message(rule=keyword(*keywords.keys()))

@demulan.handle()
async def handle_demulan(bot, event):
    for word, voice_file in keywords.items():
        if word in event.get_plaintext():
            voice_path = os.path.join("voices", voice_file)
            if os.path.exists(voice_path):
                # 读取文件并转换为 Base64
                with open(voice_path, "rb") as f:
                    voice_data = base64.b64encode(f.read()).decode("utf-8")
                # 发送 Base64 编码的语音消息
                await bot.send(event, MessageSegment.record(file=f"base64://{voice_data}"))
            else:
                await bot.send(event, f"语音文件 {voice_file} 未找到")
            break
```
<font color=DeepSkyBlue>一个非常简单的插件，用于根据关键词播放对应的语音文件。以QQ语音消息的形式发送到群聊中。这是cos德穆兰的入门级插件。</font>

2. tts2.py：
```python
from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.typing import T_State
import aiohttp
import asyncio
import base64
from pathlib import Path

# 创建命令处理器
tts2 = on_startswith("tts", priority=5, block=True)

# GPT-SOVITS API 配置
GPT_SOVITS_API_URL = "http://127.0.0.1:9880/tts"  # GPT-SOVITS API 地址
REF_AUDIO_PATH = r"E:\QQbot\voices\dml_25.wav"  # 参考音频路径
PROMPT_TEXT = "知道你在谁的地盘上吗？门卫没告诉你吗？我今天不见客。"  # 提示文本
PROMPT_LANG = "zh"  # 提示文本的语言

# 音频文件输出目录
WAV_OUTPUT_DIR = r"E:\QQbot\output2"
Path(WAV_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


async def call_gpt_sovits_api(text: str) -> bytes:
    """
    调用 GPT-SOVITS API 进行语音合成。

    Args:
        text (str): 要合成的文本。

    Returns:
        bytes: 合成的音频数据。

    Raises:
        ValueError: 如果请求参数无效或 API 返回错误。
    """
    # 构造请求参数
    payload = {
        "text": text,
        "text_lang": PROMPT_LANG,  # 文本语言
        "ref_audio_path": REF_AUDIO_PATH,  # 参考音频路径
        "prompt_text": PROMPT_TEXT,  # 提示文本
        "prompt_lang": PROMPT_LANG,  # 提示文本语言
        "text_split_method": "cut5",  # 文本分割方法
        "batch_size": 1,  # 批量大小
        "media_type": "wav",  # 输出音频格式
        "streaming_mode": False,  # 是否启用流式响应
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GPT_SOVITS_API_URL, json=payload) as response:
                if response.status == 200:
                    # 返回音频数据
                    return await response.read()
                else:
                    # 捕获 API 返回的错误信息
                    error_info = await response.json()
                    raise ValueError(f"API 返回错误: {error_info.get('message', '未知错误')}")
    except Exception as e:
        raise ValueError(f"请求 GPT-SOVITS API 失败: {str(e)}")


@tts2.handle()
async def handle_tts2(event: GroupMessageEvent, state: T_State):
    # 提取用户输入的文本
    raw_text = event.get_plaintext().strip()
    text = raw_text[len("tts"):].strip()  # 去掉开头的 "tts"

    if not text:
        await tts2.finish("请输入要合成的文本。")

    try:
        # 调用 GPT-SOVITS API 进行语音合成
        wav_data = await call_gpt_sovits_api(text)

        # 保存音频文件
        wav_path = Path(WAV_OUTPUT_DIR) / f"{event.user_id}.wav"
        with open(wav_path, "wb") as f:
            f.write(wav_data)

        # 读取 WAV 文件并转换为 Base64
        with open(wav_path, "rb") as f:
            voice_data = base64.b64encode(f.read()).decode("utf-8")
        voice_message = MessageSegment.record(file=f"base64://{voice_data}")

        # 发送语音消息
        await tts2.send(voice_message)

        # 艾特用户
        await tts2.send(MessageSegment.at(event.user_id) + " 语音合成完成！")
    except ValueError as e:
        await tts2.finish(f"语音合成失败: {str(e)}")
    except Exception as e:
        await tts2.finish(f"发生未知错误: {str(e)}")
```
<font color=HotPink>这是一个基于GPT-SOVITS API的语音合成插件，用于将用户输入的文本转换为语音并发送给用户。关于训练的部分见GPT-SOVITS云端训练的文章。
德穆兰最突出的特点就是她的正宗哈夫克口音，所以语音合成是cos德穆兰的核心功能。这里只是实现调用api和将消息转换的功能，具体合成，推理的部分还是得靠
GPT-SOVITS的api来实现。（关于api的部分也见GPT-SOVITS云端训练的文章）</font>

### 其他注意事项：

* 启动bot.py后就可以直接看到运行的端口了。
* 想要添加新的插件在bot.py中load_plugin('插件名')即可。
* 语音合成插件需要配置GPT-SOVITS API的地址，以及合成参数，具体见代码。

# <font color=DeepPink>下班！！</font>