import torch
import torch.nn as nn
#optim是用于优化器的模块，多种常用的优化算法来训练，更新模型参数以最小化损失函数
import torch.optim as optim
import torchaudio
import numpy as np
#librosa 是一个专门用于音频和音乐分析的库，
# 1.能够进行音频保存 2.音频特征提取 3.音高和节奏的分析 4.时间拉伸和音高变换，5. 显示和可视化，结合matploblib绘制频谱图，波形图
import librosa

#音频数据预处理：将音频转换为梅尔频谱图
#file_path是音频文件的路径，sr:采样率，n_mels：梅尔频谱图的梅尔频率通道数量
def load_and_preprocess_audio(file_path,sr=22050,n_mels=128):
    #加载音频文件
    y,sr=librosa.load(file_path,sr)#加载音频文件，返回音频信号y和采样率sr。如果提供了sr，则音频将被重采样到该采样率

    #计算梅尔频谱图
    mel_spectrogram=librosa.feature.melspectrogram(y,sr=sr,n_mels=n_mels)

    #将功率谱图转换为对数刻度
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram,ref=np.max) #以增强其可读性

    #转换为pytorch Tensor
    torch.tensor(log_mel_spectrogram).unsqueeze(0).unsqueeze(0) #增加一个通道维度
    return log_mel_spectrogram


#CNN模型构建
class AudioCNN(nn.modules):
    #num_classes网络的输出类别数
    def __init__(self,num_classes=10):
        super(AudioCNN,self).__init__()
        # in_channels 输入通道数1，单个对数梅尔频谱图，通道数为1
        # 输出通道数为32 表示该卷积层输出32个特征图
        self.conv1 = nn.Conv2d(1,32,kernel_size=3,stride=1,padding=1)
        #池化层
        self.pool  = nn.MaxPool2d(2,2)
        #卷积层2和卷积层3
        self.conv2=nn.Conv2d(32,64,kernel_size=3,stride=1,padding=1)
        self.conv3=nn.Conv2d(64,128,kernel_size=3,stride=1,padding=1)
        #全连接层1
        nn.Linear(128)


