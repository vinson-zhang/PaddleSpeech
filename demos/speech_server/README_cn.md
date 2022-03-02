([简体中文](./README_cn.md)|English)

# 语音服务

## 介绍
这个demo是一个启动语音服务和访问服务的实现。 它可以通过使用`paddlespeech_server` 和 `paddlespeech_client`的单个命令或 python 的几行代码来实现。


## 使用方法
### 1. 安装
请看 [安装文档](https://github.com/PaddlePaddle/PaddleSpeech/blob/develop/docs/source/install.md).

你可以从 easy，medium，hard 三中方式中选择一种方式安装 PaddleSpeech。

### 2. 准备配置文件
配置文件包含服务相关的配置文件和服务中包含的语音任务相关的模型配置。 它们都在 `conf` 文件夹下。
**注意：`application.yaml` 中 `engine_backend` 的配置表示启动的服务中包含的所有语音任务。**
如果你想启动的服务中只包含某项语音任务，那么你需要注释掉不需要包含的语音任务。例如你只想使用语音识别（ASR）服务，那么你可以将语音合成（TTS）服务注释掉，如下示例：
```bash
engine_backend:
    asr: 'conf/asr/asr.yaml'
    #tts: 'conf/tts/tts.yaml'
```
**注意：`application.yaml` 中 `engine_backend` 的配置文件需要和 `engine_type` 的配置类型匹配。**
当`engine_backend` 的配置文件为`XXX.yaml`时，需要设置`engine_type`的配置类型为`python`;当`engine_backend` 的配置文件为`XXX_pd.yaml`时，需要设置`engine_type`的配置类型为`inference`;

这个 ASR client 的输入应该是一个 WAV 文件（`.wav`），并且采样率必须与模型的采样率相同。

可以下载此 ASR client的示例音频：
```bash
wget -c https://paddlespeech.bj.bcebos.com/PaddleAudio/zh.wav https://paddlespeech.bj.bcebos.com/PaddleAudio/en.wav
```

### 3. 服务端使用方法
- 命令行 (推荐使用)

  ```bash
  # 启动服务
  paddlespeech_server start --config_file ./conf/application.yaml
  ```

  使用方法：
  
  ```bash
  paddlespeech_server start --help
  ```
  参数:
  - `config_file`: 服务的配置文件，默认： ./conf/application.yaml
  - `log_file`: log 文件. 默认：./log/paddlespeech.log

  输出:
  ```bash
  [2022-02-23 11:17:32] [INFO] [server.py:64] Started server process [6384]
  INFO:     Waiting for application startup.
  [2022-02-23 11:17:32] [INFO] [on.py:26] Waiting for application startup.
  INFO:     Application startup complete.
  [2022-02-23 11:17:32] [INFO] [on.py:38] Application startup complete.
  INFO:     Uvicorn running on http://0.0.0.0:8090 (Press CTRL+C to quit)
  [2022-02-23 11:17:32] [INFO] [server.py:204] Uvicorn running on http://0.0.0.0:8090 (Press CTRL+C to quit)

  ```

- Python API
  ```python
  from paddlespeech.server.bin.paddlespeech_server import ServerExecutor

  server_executor = ServerExecutor()
  server_executor(
      config_file="./conf/application.yaml", 
      log_file="./log/paddlespeech.log")
  ```

  输出：
  ```bash
  INFO:     Started server process [529]
  [2022-02-23 14:57:56] [INFO] [server.py:64] Started server process [529]
  INFO:     Waiting for application startup.
  [2022-02-23 14:57:56] [INFO] [on.py:26] Waiting for application startup.
  INFO:     Application startup complete.
  [2022-02-23 14:57:56] [INFO] [on.py:38] Application startup complete.
  INFO:     Uvicorn running on http://0.0.0.0:8090 (Press CTRL+C to quit)
  [2022-02-23 14:57:56] [INFO] [server.py:204] Uvicorn running on http://0.0.0.0:8090 (Press CTRL+C to quit)

  ```

### 4. ASR客户端使用方法
**注意：**初次使用客户端时响应时间会略长
- 命令行 (推荐使用)
   ```
   paddlespeech_client asr --server_ip 127.0.0.1 --port 8090 --input ./zh.wav
   ```

    使用帮助:
  
    ```bash
    paddlespeech_client asr --help
    ```

    参数:
    - `server_ip`: 服务端ip地址，默认: 127.0.0.1。
    - `port`: 服务端口，默认: 8090。
    - `input`(必须输入): 用于识别的音频文件。
    - `sample_rate`: 音频采样率，默认值：16000。
    - `lang`: 模型语言，默认值：zh_cn。
    - `audio_format`: 音频格式，默认值：wav。

    输出:

    ```bash
    [2022-02-23 18:11:22,819] [    INFO] - {'success': True, 'code': 200, 'message': {'description': 'success'}, 'result': {'transcription': '我认为跑步最重要的就是给我带来了身体健康'}}
    [2022-02-23 18:11:22,820] [    INFO] - time cost 0.689145 s.
    ```

- Python API
  ```python
  from paddlespeech.server.bin.paddlespeech_client import ASRClientExecutor

  asrclient_executor = ASRClientExecutor()
  asrclient_executor(
      input="./zh.wav",
      server_ip="127.0.0.1",
      port=8090,
      sample_rate=16000,
      lang="zh_cn",
      audio_format="wav")
  ```

  输出:
  ```bash
  {'success': True, 'code': 200, 'message': {'description': 'success'}, 'result': {'transcription': '我认为跑步最重要的就是给我带来了身体健康'}}
  time cost 0.604353 s.

  ```
 
### 5. TTS客户端使用方法
**注意：**初次使用客户端时响应时间会略长
   ```bash
   paddlespeech_client tts --server_ip 127.0.0.1 --port 8090 --input "您好，欢迎使用百度飞桨语音合成服务。" --output output.wav
   ```
    使用帮助:
  
    ```bash
    paddlespeech_client tts --help
    ```

    参数:
    - `server_ip`: 服务端ip地址，默认: 127.0.0.1。
    - `port`: 服务端口，默认: 8090。
    - `input`(必须输入): 待合成的文本。
    - `spk_id`: 说话人 id，用于多说话人语音合成，默认值： 0。
    - `speed`: 音频速度，该值应设置在 0 到 3 之间。 默认值：1.0
    - `volume`: 音频音量，该值应设置在 0 到 3 之间。 默认值： 1.0
    - `sample_rate`: 采样率，可选 [0, 8000, 16000]，默认与模型相同。 默认值：0
    - `output`: 输出音频的路径， 默认值：output.wav。

    输出:
    ```bash
    [2022-02-23 15:20:37,875] [    INFO] - {'description': 'success.'}
    [2022-02-23 15:20:37,875] [    INFO] - Save synthesized audio successfully on output.wav.
    [2022-02-23 15:20:37,875] [    INFO] - Audio duration: 3.612500 s.
    [2022-02-23 15:20:37,875] [    INFO] - Response time: 0.348050 s.
    ```

- Python API
  ```python
  from paddlespeech.server.bin.paddlespeech_client import TTSClientExecutor

  ttsclient_executor = TTSClientExecutor()
  ttsclient_executor(
      input="您好，欢迎使用百度飞桨语音合成服务。",
      server_ip="127.0.0.1",
      port=8090,
      spk_id=0,
      speed=1.0,
      volume=1.0,
      sample_rate=0,
      output="./output.wav")
  ```

  输出:
  ```bash
  {'description': 'success.'}
  Save synthesized audio successfully on ./output.wav.
  Audio duration: 3.612500 s.
  Response time: 0.388317 s.

  ```

## 服务支持的模型
### ASR支持的模型
通过 `paddlespeech_server stats --task asr` 获取ASR服务支持的所有模型，其中静态模型可用于 paddle inference 推理。 

### TTS支持的模型
通过 `paddlespeech_server stats --task tts` 获取TTS服务支持的所有模型，其中静态模型可用于 paddle inference 推理。