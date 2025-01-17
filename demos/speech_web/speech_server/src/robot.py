from paddlespeech.cli.asr.infer import ASRExecutor
import soundfile as sf
import os
import librosa

from src.SpeechBase.asr import ASR
from src.SpeechBase.tts import TTS
from src.SpeechBase.nlp import NLP


class Robot:
    def __init__(self, asr_config, tts_config,asr_init_path,
                 ie_model_path=None) -> None:
        self.nlp = NLP(ie_model_path=ie_model_path)
        self.asr = ASR(config_path=asr_config)
        self.tts = TTS(config_path=tts_config)
        self.tts_sample_rate = 24000
        self.asr_sample_rate = 16000
        
        # 流式识别效果不如端到端的模型，这里流式模型与端到端模型分开
        self.asr_model = ASRExecutor()
        self.asr_name = "conformer_wenetspeech"
        self.warm_up_asrmodel(asr_init_path)
        

    def warm_up_asrmodel(self, asr_init_path):        
        if not os.path.exists(asr_init_path):
            path_dir = os.path.dirname(asr_init_path)
            if not os.path.exists(path_dir):
                os.makedirs(path_dir, exist_ok=True)
            
            # TTS生成，采样率24000
            text = "生成初始音频"
            self.text2speech(text, asr_init_path)
            
        # asr model初始化
        self.asr_model(asr_init_path, model=self.asr_name,lang='zh',
                 sample_rate=16000)
        
    
    def speech2text(self, audio_file):
        self.asr_model.preprocess(self.asr_name, audio_file)
        self.asr_model.infer(self.asr_name)
        res = self.asr_model.postprocess()
        return res
    
    def text2speech(self, text, outpath):
        wav = self.tts.offlineTTS(text)
        sf.write(
            outpath, wav, samplerate=self.tts_sample_rate)
        res = wav
        return res
    
    def text2speechStream(self, text):
        for sub_wav_base64 in self.tts.streamTTS(text=text):
            yield sub_wav_base64
    
    def text2speechStreamBytes(self, text):
        for wav_bytes in self.tts.streamTTSBytes(text=text):
            yield wav_bytes

    def chat(self, text):
        result = self.nlp.chat(text)
        return result

    def ie(self, text):
        result = self.nlp.ie(text)
        return result
    
if __name__ == '__main__':
    tts_config = "../PaddleSpeech/demos/streaming_tts_server/conf/tts_online_application.yaml"
    asr_config = "../PaddleSpeech/demos/streaming_asr_server/conf/ws_conformer_application.yaml"
    demo_wav = "../source/demo/demo_16k.wav"
    ie_model_path = "../source/model"
    tts_wav = "../source/demo/tts.wav"
    text = "今天天气真不错"
    ie_text = "今天晚上我从大牛坊出发去三里屯花了六十五块钱"
    
    
    robot = Robot(asr_config, tts_config, asr_init_path=demo_wav)
    res = robot.speech2text(demo_wav)
    print(res)
    
    res = robot.chat(text)
    print(res)
    print("tts offline")
    robot.text2speech(res, tts_wav)
    
    print("ie test")
    res = robot.ie(ie_text)
    print(res)
    
    