import librosa
import soundfile,time
import os,glob,pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
def mainrun():
    def extract_feature(file_name, mfcc, chroma, mel):
        with soundfile.SoundFile(file_name) as sound_file:
            X = sound_file.read(dtype="float32")
            sample_rate=sound_file.samplerate
            if chroma:
                stft=np.abs(librosa.stft(X))
            result = np.array([])
            if mfcc:
                mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
                result=np.hstack((result,mfccs))
            if chroma:
                chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
                result=np.hstack((result,chroma))
            if mel:
                mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)
                result = np.hstack((result, mel))
        return result

    emotions={
        '01':'neutral',
        '02':'calm',
        '03':'happy',
        '04':'sad',
        '05':'angry',
        '06':'fearful',
        '07':'disgust',
        '08':'surprised',
    }
    #Emotions to observe
    observed_emotions=['calm','happy','fearful','disgust']
    #Load the Data and extract Features for each sound file
    def load_data(test_size=0.2):
        x,y=[],[]
        for file in glob.glob("Actor_*\\*.wav"):
            file_name=os.path.basename(file)
            emotion=emotions[file_name.split("-")[2]]
            if emotion not in observed_emotions:
                continue
            feature=extract_feature(file,mfcc=True,chroma=True,mel=True)
            x.append(feature)
            y.append(emotion)
        return train_test_split(np.array(x), y, test_size=test_size,random_state=9)

    file="SubmitAudio.wav"
    feature=extract_feature(file, mfcc=True, chroma=True, mel=True)

    x_train,x_test,y_train,y_test=load_data(test_size=0.25)
    print(x_train)
    print(x_test)
    print(y_train)
    print(y_test)

    model=MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500)

    model.fit(x_train,y_train)

    y_pred=model.predict(x_test)
    y_pre=model.predict([feature])

    print(y_pre)
    observed_emotion=y_pre[0]
    if y_pre[0] == "calm":
        url=("https://open.spotify.com/playlist/1Dk9SeguLL5qTnjfyX5VnZ?si=kKVGBE2cQdmJHotuH83moQ")
    elif y_pre[0] == "neutral":
        url=("https://open.spotify.com/playlist/3XIpkr0wzAsRQFCtMWfuTq?si=hsL-P1ymT0mruY3eWoSEVA")
    elif y_pre[0] == "happy":
        url=("https://open.spotify.com/playlist/78kBHYaQsF6zntWU9R6ziQ?si=nvNbVmI5S9m8Ef3_HR15AQ")
    elif y_pre[0] == "sad":
        url=("https://open.spotify.com/playlist/5I9As02pKBVN1kONkCX71l?si=EvjUzllSS4qm6CoiEu7dOA")
    elif y_pre[0] == "angry":
        url=("https://open.spotify.com/playlist/0s5O323LN8dpV81h33OoZQ?si=z3fEy4yxTBexeHJ8Snrsrw")
    elif y_pre[0] == "fearful":
        url=("https://open.spotify.com/playlist/1Dk9SeguLL5qTnjfyX5VnZ?si=kKVGBE2cQdmJHotuH83moQ")
    elif y_pre[0] == "disgust":
        url="https://open.spotify.com/playlist/3XIpkr0wzAsRQFCtMWfuTq?si=hsL-P1ymT0mruY3eWoSEVA"
    return url
    #time.sleep(2)








"""import webbrowser

if y_pre[0]=="calm":
    webbrowser.open("https://www.youtube.com/watch?v=7OE_9Bwholk")
elif y_pre[0]=="neutral":
    webbrowser.open("https://www.youtube.com/watch?v=lFcSrYw-ARY")
elif y_pre[0]=="happy":
    webbrowser.open("https://www.youtube.com/watch?v=ru0K8uYEZWw&ab_channel=justintimberlakeVEVO    ")
elif y_pre[0]=="sad":
    webbrowser.open("https://www.youtube.com/watch?v=ZbZSe6N_BXs")
elif y_pre[0]=="angry":
    webbrowser.open("https://www.youtube.com/watch?v=ZbZSe6N_BXs")
elif y_pre[0]=="fearful":
    webbrowser.open("https://www.youtube.com/watch?v=ZbZSe6N_BXs")
elif y_pre[0]=="disgust":
    webbrowser.open("https://www.youtube.com/watch?v=ZbZSe6N_BXs")"""

