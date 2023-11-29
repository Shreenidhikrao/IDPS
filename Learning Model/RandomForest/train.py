import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the dataset
data = pd.read_csv("/mnt/D0F8D669F8D64CFA/Capstone_project/NSL-KDD/KDDTrain+.txt")

# Rest of the code for preprocessing and feature engineering

columns = (['duration'
,'protocol_type'
,'service'
,'flag'
,'src_bytes'
,'dst_bytes'
,'land'
,'wrong_fragment'
,'urgent'
,'hot'
,'num_failed_logins'
,'logged_in'
,'num_compromised'
,'root_shell'
,'su_attempted'
,'num_root'
,'num_file_creations'
,'num_shells'
,'num_access_files'
,'num_outbound_cmds'
,'is_host_login'
,'is_guest_login'
,'count'
,'srv_count'
,'serror_rate'
,'srv_serror_rate'
,'rerror_rate'
,'srv_rerror_rate'
,'same_srv_rate'
,'diff_srv_rate'
,'srv_diff_host_rate'
,'dst_host_count'
,'dst_host_srv_count'
,'dst_host_same_srv_rate'
,'dst_host_diff_srv_rate'
,'dst_host_same_src_port_rate'
,'dst_host_srv_diff_host_rate'
,'dst_host_serror_rate'
,'dst_host_srv_serror_rate'
,'dst_host_rerror_rate'
,'dst_host_srv_rerror_rate'
,'attack'
,'level'])

data.columns = columns
data.head()


unwanted_cols = ['land'
,'wrong_fragment'
,'urgent'
,'hot'
,'num_failed_logins'
,'logged_in'
,'num_compromised'
,'root_shell'
,'su_attempted'
,'num_root'
,'num_file_creations'
,'num_shells'
,'num_access_files'
,'num_outbound_cmds'
,'is_host_login'
,'is_guest_login'
,'count'
,'srv_count'
,'serror_rate'
,'srv_serror_rate'
,'rerror_rate'
,'srv_rerror_rate'
,'same_srv_rate'
,'diff_srv_rate'
,'srv_diff_host_rate'
,'dst_host_count'
,'dst_host_srv_count'
,'dst_host_same_srv_rate'
,'dst_host_diff_srv_rate'
,'dst_host_same_src_port_rate'
,'dst_host_srv_diff_host_rate'
,'dst_host_serror_rate'
,'dst_host_srv_serror_rate'
,'dst_host_rerror_rate'
,'dst_host_srv_rerror_rate'] 

data = data.drop(unwanted_cols, axis=1)
data.head()

is_attack = data.attack.map(lambda a: 0 if a == 'normal' else 1)
data['attack_flag'] = is_attack
data.head()

# Define categorical columns
categorical_cols = ['protocol_type', 'service', 'flag']  # Categorical columns in the dataset
label_encoder = LabelEncoder()
data['encoded_label'] = label_encoder.fit_transform(data['attack'])  
data.head()

# ... (your code for Label Encoding and OneHot Encoding)

onehot_encoder = OneHotEncoder(sparse_output=False)
encoded_categorical_cols = pd.DataFrame(onehot_encoder.fit_transform(data[categorical_cols]))
encoded_categorical_cols.columns = onehot_encoder.get_feature_names_out(categorical_cols)

data_encoded = pd.concat([data.drop(categorical_cols + ['attack'], axis=1), encoded_categorical_cols], axis=1)

X = data_encoded.drop(['encoded_label'], axis=1)  # Features
y = data_encoded['encoded_label']  # Target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

n_estimators = 100  # Number of trees in the forest
classifier = RandomForestClassifier(n_estimators=n_estimators)

# Fit the model
classifier.fit(X_train, y_train)

# Evaluate the model
accuracy = classifier.score(X_test, y_test)
print("Accuracy:", accuracy)



import pickle
# Save the classifier and necessary variables to a pickle file
with open('random_forest.pkl', 'wb') as file:
    pickle.dump(classifier, file)
    pickle.dump(label_encoder, file)
    pickle.dump(onehot_encoder, file)
    pickle.dump(categorical_cols, file)
    pickle.dump(data_encoded,file)
    pickle.dump(X,file)
    pickle.dump(y,file)

print("\nPickle file created in the same directory as this program.")