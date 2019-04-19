
### MNiST 데이터셋을 훈련용(TrainingSet) 60,000개와 테스트용(TestSet) 10,000로 훈련 및 검증하고, 학습된 모델을 재사용 가능하도록, clf instance 파일로 serialize하기.
~~~python 

from sklearn import svm, metrics
import pandas as pd
from sklearn.externals import joblib
from pathlib import Path
from sklearn.model_selection import GridSearchCV

def readCsv(file, maxcnt):
    labels = []
    images = []
    with open(file, "r") as f:
        for i, line in enumerate(f):
            if i >= maxcnt:
                break
            cols = line.split(",")
            labels.append(int(cols.pop(0)))     
            images.append(list(map(lambda b: int(b) / 256, cols)))  # 실수 벡터화
    return {"labels": labels, "images": images}


test = readCsv('./data/t10k.csv', 10000)

pklFile = "./data/mnist.pkl"
clf = None
if Path(pklFile).exists():              
    print("File Exists!!")
    clf = joblib.load(pklFile)


# 학습
if not clf:
    train = readCsv('./data/train.csv', 60000)   
    clf = svm.SVC(gamma='auto')
    print(len(train['labels']))
    clf.fit(train['images'], train['labels'])
    joblib.dump(clf, pklFile)


# 검증
pred = clf.predict(test['images'])

score = metrics.accuracy_score(test['labels'], pred)
print("\n\nscore=", score)

report = metrics.classification_report(test['labels'], pred)
print(report)

~~~

<br>


### 붓꽃 데이터셋(iris.csv)을 SVM으로 학습시킬 때, 최적의 모델을 찾기위한 SVC 매개변수 찾기.
~~~python 

from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

csv = pd.read_csv('./data/iris.csv')

cdata = csv[['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']]
cret = csv['Name']

trainData, testData, trainLabel, testLabel = train_test_split(cdata, cret)

params = [
    {"C": [1, 10, 100, 1000], "kernel": ['linear']},
    {"C": [1, 10, 100, 1000], "kernel": ['rbf'], "gamma": [0.001, 0.0001]},
]

clf = GridSearchCV(svm.SVC(), params, n_jobs = 2, cv = 3, iid=True)

clf.fit(trainData, trainLabel)   

print("machine=", clf.best_estimator_)


~~~
