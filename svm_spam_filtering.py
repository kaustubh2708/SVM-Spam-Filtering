# -*- coding: utf-8 -*-
"""svm-spam-filtering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fPF8ZY8tHXxgTkXSe59mB0TsQiUROotY

# **CAT -3 PREDICTIVE ANALYSIS**

#  Implement Support Vector Machine to build a spam classifier

##  Import required libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn import feature_extraction, model_selection, naive_bayes, metrics, svm
from IPython.display import Image
import warnings
warnings.filterwarnings("ignore")
# %matplotlib inline

"""## Exploring the Dataset"""

data = pd.read_csv('/spam.csv', encoding='latin-1')
data.head(n=10)

"""## Describe the Data Set"""

data.info()

"""## Distribution spam/non-spam plots"""

count_Class=pd.value_counts(data["v1"], sort= True)
count_Class.plot(kind= 'bar', color= ["blue", "orange"])
plt.title('Bar chart')
plt.show()

count_Class.plot(kind = 'pie', shadow=True,explode=(0,0.1), autopct='%1.1f%%')
plt.title('Pie chart')
plt.ylabel('')
plt.show()

"""## Text Analytics

We want to find the frequencies of words in the spam and non-spam messages. The words of the messages will be model features.<p>
We use the function Counter.
"""

count1 = Counter(" ".join(data[data['v1']=='ham']["v2"]).split()).most_common(20)
df1 = pd.DataFrame.from_dict(count1)
df1 = df1.rename(columns={0: "words in non-spam", 1 : "count"})
count2 = Counter(" ".join(data[data['v1']=='spam']["v2"]).split()).most_common(20)
df2 = pd.DataFrame.from_dict(count2)
df2 = df2.rename(columns={0: "words in spam", 1 : "count_"})

df1.plot.bar(legend = False)
y_pos = np.arange(len(df1["words in non-spam"]))
plt.xticks(y_pos, df1["words in non-spam"])
plt.title('More frequent words in non-spam messages')
plt.xlabel('words')
plt.ylabel('number')
plt.show()

df2.plot.bar(legend = False, color = 'orange')
y_pos = np.arange(len(df2["words in spam"]))
plt.xticks(y_pos, df2["words in spam"])
plt.title('More frequent words in spam messages')
plt.xlabel('words')
plt.ylabel('number')
plt.show()

"""#### We can see that the majority of frequent words in both classes are stop words such as 'to', 'a', 'or' and so on.

#### With stop words we refer to the most common words in a language, there is no single, universal list of stop words.

## **Predictive Analysis**

#### **Our goal is to predict if a new sms is spam or non-spam. We assume that is much worse misclassify non-spam than misclassify an spam. (We want to have minimum number of false positives)**


#### This model should get lowest possible number of spam message in our inbox(False Negative) and lowest number of non spam message in the spam folder(False Positive).

#### First we transform the variable spam/non-spam into binary variable(assigning binary values 0 to non spam mails and 1 to spam mails), then we split our data set in training set and test set.
"""

data["v1"]=data["v1"].map({'spam':1,'ham':0})
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, data['v1'], test_size=0.33, random_state=42)
print([np.shape(X_train), np.shape(X_test)])

"""## **Support Vector Machine**

#### We are going to apply the same reasoning applying the support vector machine model with the gaussian kernel.

#### We train different models changing the regularization parameter C.

#### We evaluate the accuracy, recall and precision of the model with the test set.
"""

list_C = np.arange(500, 2000, 100) #100000
score_train = np.zeros(len(list_C))
score_test = np.zeros(len(list_C))
recall_test = np.zeros(len(list_C))
precision_test= np.zeros(len(list_C))
count = 0
for C in list_C:
    svc = svm.SVC(C=C)
    svc.fit(X_train, y_train)
    score_train[count] = svc.score(X_train, y_train)
    score_test[count]= svc.score(X_test, y_test)
    recall_test[count] = metrics.recall_score(y_test, svc.predict(X_test))
    precision_test[count] = metrics.precision_score(y_test, svc.predict(X_test))
    count = count + 1

"""#### Now let's look at our learning model and its metrics"""

matrix = np.matrix(np.c_[list_C, score_train, score_test, recall_test, precision_test])
models = pd.DataFrame(data = matrix, columns = 
             ['C', 'Train Accuracy', 'Test Accuracy', 'Test Recall', 'Test Precision'])
models.head(n=10)

"""#### Checking for model with highest precision"""

best_index = models['Test Precision'].idxmax()
models.iloc[best_index, :]

"""#### Now we see if there are more than 1 model available with the highest precision(99.5%)"""

models[models['Test Precision']>=0.995].head(n=20)

"""#### Between these models with the highest possible precision, we are going to selct which has more test accuracy."""

best_index = models[models['Test Precision']>=0.995]['Test Accuracy'].idxmax()
svc = svm.SVC(C=list_C[best_index])
svc.fit(X_train, y_train)
models.iloc[best_index, :]

"""### **Confusion matrix with support vector machine classifier.**"""

m_confusion_test = metrics.confusion_matrix(y_test, svc.predict(X_test))
pd.DataFrame(data = m_confusion_test, columns = ['Predicted 0', 'Predicted 1'],
            index = ['Actual 0', 'Actual 1'])

"""#### We misclassify 37 spam as non-spam messages and we misclassify 1 non-spam message.

### **Accuracy**
"""

svc.score(X_test,y_test)

"""#### Here we are getting accuracy of 97.93%"""