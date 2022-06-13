import pandas as pd
from sklearn.utils import resample
import matplotlib.pyplot as plt

#encoding categorical variables to numeric ones
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, auc

"""

    loading the data into pandas dataframe

"""

activity = pd.read_csv('./data/activity.csv')
target = pd.read_csv('./data/target.csv')
"""

    Observing the data

"""
# print(activity.head())
# print(activity.size)
# print(target.head())
# print(target.size)
# print(activity.info())
# print(target.info())

###### data labeling ########
target['label'] = 1
print("target",target)

############ value count ##########
print("activity Count",activity['activity_count'].value_counts())
print("customer",activity['customer'].value_counts())
print("activity type",activity['activity_type'].value_counts())

"""

    Merging the both dataframe together.

"""
activity_new = pd.merge(activity, target, on=['customer', 'date'], how='left')
activity_new = activity_new.fillna(0)

print(activity_new)

print(activity_new['label'].value_counts())

"""

    Data downsampling

"""
activity_new_majority = activity_new[activity_new.label==0]
activity_new_minority = activity_new[activity_new.label==1]

activity_new_majority_upsampled = resample(activity_new_minority, 
                                replace=True,    # sample without replacement
                                n_samples=800000,     # to match minority class
                                random_state=123) # reproducible results

# Combine minority class with downsampled majority class
activity_new_upsampled = pd.concat([activity_new_majority_upsampled, activity_new_majority])

activity_new_upsampled = activity_new_upsampled.drop(['date', 'customer', 'activity_count'], axis=1)

print("####################",activity_new_upsampled)



########## categorical to numeric #############
def obj_to_num(df):
    for c in df.columns:
        if df[c].dtype=='object':    
            lbl = LabelEncoder()
            lbl.fit(list(df[c].values))
            df[c] = lbl.transform(df[c].values)
    return df

activity_new_upsampled = obj_to_num(activity_new_upsampled)
print(activity_new_upsampled)


activity_new_upsampled['activity_type'].value_counts()

########### Separating the dataset as response variable and feature variables

X = activity_new_upsampled.drop('label', axis = 1)
y = activity_new_upsampled['label']

########### Train and Test splitting of data

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, stratify=y, random_state = 42)

print("1111111111111",X_train)
print("2222222222222",X_test)
print("3333333333333",y_train)
print("444444444444",y_test)



########### Applying Standard scaling

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

print(X_train)
print(X_test)



"""### Random Forest"""
print("################# Random Forest ################")

rfc = RandomForestClassifier(n_estimators=300)

rfc.fit(X_train, y_train)
pred_rfc = rfc.predict(X_test)

###### Checking Model Performance
print("Classification Matrix:")
print(classification_report(y_test, pred_rfc))
print("Cofusion Matrix:")
cm = confusion_matrix(y_test, pred_rfc)
print(cm)
print("accuracy 0 and 1",cm.diagonal()/cm.sum(axis=1))

"""### Logistic Regression"""

print("################# Logistic Regression ################")

lReg = LogisticRegression(penalty='l2',tol=0.001,random_state=0)
lReg.fit(X_train, y_train)
pred_lReg = lReg.predict(X_test)

####### Checking Model Performance
print("Classification Matrix:")
print(classification_report(y_test, pred_lReg))
print("Cofusion Matrix:")
cm_lReg = confusion_matrix(y_test, pred_lReg)
print("accuracy 0 and 1",cm_lReg.diagonal()/cm_lReg.sum(axis=1))

"""### SVM classifier"""

print("################# Support Vector Machine ################")

sv = SVC(tol = 0.0001)
sv.fit(X_train, y_train)
pred_sv = sv.predict(X_test)

####### Checking Model Performance
print("Classification Matrix:")
print(classification_report(y_test, pred_sv))
print("Cofusion Matrix:")
cm = confusion_matrix(y_test, pred_sv)
print(cm)
print("accuracy 0,1",cm.diagonal()/cm.sum(axis=1))

"""### Gradient Boost"""

print("################# Gradient Boost ################")

gboost = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
gboost.fit(X_train, y_train)
pred_gboost = gboost.predict(X_test)

####### Checking Model Performance
print("Classification Matrix:")
print(classification_report(y_test, pred_gboost))
print("Cofusion Matrix:")
cm = confusion_matrix(y_test, pred_gboost)
print(cm)
print("accuracy 0,1",cm.diagonal()/cm.sum(axis=1))

"""### Neural Network"""

print("################# MLP Classifier ################")

mlpc = MLPClassifier(hidden_layer_sizes=(25,25,25), max_iter=500)
mlpc.fit(X_train, y_train)
pred_mlpc = mlpc.predict(X_test)

####### Checking Model Performance
print("Classification Matrix:")
print(classification_report(y_test, pred_mlpc))
print("Cofusion Matrix:")
cm = confusion_matrix(y_test, pred_mlpc)
print(cm)
print("accuracy 0,1",cm.diagonal()/cm.sum(axis=1))