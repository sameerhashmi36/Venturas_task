import pandas as pd
from sklearn.utils import resample

"""

    loading the data into pandas dataframe

"""
activity = pd.read_csv('./data/activity.csv')
target = pd.read_csv('./data/target.csv')

"""

    Observing the data

"""
print(activity.head())
print(activity.size)
print(target.head())
print(target.size)
print(activity.info())
print("unique customers: ",activity['customer'].describe())
print(target.info())

###### data labeling ########
target['label'] = 1
print(target)

############ value count ##########
print(activity['activity_count'].value_counts())
print(activity['date'].value_counts())
print(activity['activity_type'].value_counts())

"""

    Merging the both dataframe together.

    Here the data given in target.csv which are already closed activity with the customers are labeled 1
    and the other data are labeled 0

"""

activity_new = pd.merge(activity, target, on=['customer', 'date'], how='left')
activity_new = activity_new.fillna(0)

print(activity_new)

print(activity_new['label'].value_counts())

"""

    Sanity Check

"""
activities = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y']
for i in activities:
  print("#####",i,"#####")
  filt = activity_new['activity_type'] == i
  print(activity_new.loc[filt]['label'].value_counts())

print("Activity_new Describe: ",activity_new.describe())

"""### Down Sample data distribution Check"""

activity_new_majority = activity_new[activity_new.label==0]
activity_new_minority = activity_new[activity_new.label==1]

activity_new_majority_downsampled = resample(activity_new_majority, 
                                 replace=False,    # sample without replacement
                                 n_samples=13694,     # to match minority class
                                 random_state=123) # reproducible results

# Combine minority class with downsampled majority class
activity_new_downsampled = pd.concat([activity_new_majority_downsampled, activity_new_minority])

for i in activities:
  print("#####",i,"#####")
  filt = activity_new_downsampled['activity_type'] == i
  print(activity_new_downsampled.loc[filt]['label'].value_counts())

"""### Up Sample Data Distribution Check"""

from sklearn.utils import resample

activity_new_majority = activity_new[activity_new.label==0]
activity_new_minority = activity_new[activity_new.label==1]

activity_new_minority_downsampled = resample(activity_new_minority, 
                                 replace=True,    # sample without replacement
                                 n_samples=891078,     # to match minority class
                                 random_state=123) # reproducible results

# Combine minority class with downsampled majority class
activity_new_upsampled = pd.concat([activity_new_minority_downsampled, activity_new_majority])


for i in activities:
  print("#####",i,"#####")
  filt = activity_new_upsampled['activity_type'] == i
  print(activity_new_upsampled.loc[filt]['label'].value_counts())

"""### Algorithm Observation"""

values = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for i in values:
  print("##### Normal Data: ",i,"#####")
  filt = activity_new['activity_type'] == i
  print(activity_new.loc[filt]['label'].value_counts())
  print("##### Down Sampled Data: ",i,"#####")
  filt1 = activity_new_downsampled['activity_type'] == i
  print(activity_new_downsampled.loc[filt1]['label'].value_counts())
  print("##### Up Sampled Data: ",i,"#####")
  filt2 = activity_new_upsampled['activity_type'] == i
  print(activity_new_upsampled.loc[filt2]['label'].value_counts())



""" 

    Evaluating the activities 


"""
activities = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y']
important_activities = []
values = []
for i in activities:
  x, y = 0,0
  print("##### Down Sampled Data: ",i,"#####")
  filt = activity_new_downsampled['activity_type'] == i
  try:
    x = activity_new_downsampled.loc[filt]['label'].value_counts()[0]
    print("X: ",x)
  except:
    pass
  try:
    y = activity_new_downsampled.loc[filt]['label'].value_counts()[1]
    print("Y: ",y)
  except:
    pass
  if x>y:
    print("x, y", x,y)
    print("x is higher than y: ",(x/y))
    label = 0
    values.append(label)
    print(values)
  elif y>x:
    print("x, y", x,y)
    print("y is higher than x: ",(y/x))
    label = 1
    values.append(label)
    important_activities.append(i)
    print("important activities are: ",important_activities)
  else:
    label = 0
    values.append(label)

# print("555555555",values)

activity_df = pd.DataFrame({'activity_type': activities, 'contribution': values})

print(activity_df)

######### Dataframe to CSV ##########

activity_df.to_csv('./csv_file/activities.csv', sep=',', columns=['activity_type','contribution'], index=False)