import pandas as pd
import pickle

# Load the pickle file
with open('random_forest.pkl', 'rb') as file:
    classifier = pickle.load(file)
    label_encoder = pickle.load(file)
    onehot_encoder = pickle.load(file)
    categorical_cols = pickle.load(file)
    data_encoded=pickle.load(file)
    X=pickle.load(file)


test_input = ['tcp', 'http', 'SF','1','146', '1','19', '11' , '1']

real_input = [test_input[:3]]
real_input_others = test_input[3:]


real_time_input_df = pd.DataFrame(real_input, columns=categorical_cols)
encoded_real_time_input = pd.DataFrame(onehot_encoder.transform(real_time_input_df))
encoded_real_time_input.columns = onehot_encoder.get_feature_names_out(categorical_cols)

import itertools

missing_cols = set(data_encoded.columns) - set(encoded_real_time_input.columns)
values_cycle = itertools.cycle(real_input_others)
missing_cols_sorted = sorted(missing_cols)
print("\n",missing_cols_sorted)
for col in missing_cols_sorted:
    value = next(values_cycle)
    encoded_real_time_input[col] = value

encoded_real_time_input = encoded_real_time_input[X.columns]


prediction = classifier.predict(encoded_real_time_input)

predicted_label = label_encoder.inverse_transform(prediction)

print("\nPredicted Label:", predicted_label[0], "\n")