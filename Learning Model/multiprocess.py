import multiprocessing
from collections import Counter
import pandas as pd
import pickle


def algorithm1(input_data):
    with open('decision_tree_classifier.pkl', 'rb') as file:
        classifier = pickle.load(file)
        label_encoder = pickle.load(file)
        onehot_encoder = pickle.load(file)
        categorical_cols = pickle.load(file)
        data_encoded=pickle.load(file)
        X=pickle.load(file)


    real_input = [input_data[:3]]
    real_input_others = input_data[3:]


    real_time_input_df = pd.DataFrame(real_input, columns=categorical_cols)
    encoded_real_time_input = pd.DataFrame(onehot_encoder.transform(real_time_input_df))
    encoded_real_time_input.columns = onehot_encoder.get_feature_names_out(categorical_cols)

    import itertools

    missing_cols = set(data_encoded.columns) - set(encoded_real_time_input.columns)
    values_cycle = itertools.cycle(real_input_others)
    missing_cols_sorted = sorted(missing_cols)
    for col in missing_cols_sorted:
        value = next(values_cycle)
        encoded_real_time_input[col] = value
    encoded_real_time_input = encoded_real_time_input[X.columns]
    prediction = classifier.predict(encoded_real_time_input)
    predicted_label = label_encoder.inverse_transform(prediction)
    print("\nPredicted Label:", predicted_label[0])
    return predicted_label


def algorithm2(input_data):
    with open('knn_classifier.pkl', 'rb') as file:
        classifier = pickle.load(file)
        label_encoder = pickle.load(file)
        onehot_encoder = pickle.load(file)
        categorical_cols = pickle.load(file)
        data_encoded=pickle.load(file)
        X=pickle.load(file)


    real_input = [input_data[:3]]
    real_input_others = input_data[3:]


    real_time_input_df = pd.DataFrame(real_input, columns=categorical_cols)
    encoded_real_time_input = pd.DataFrame(onehot_encoder.transform(real_time_input_df))
    encoded_real_time_input.columns = onehot_encoder.get_feature_names_out(categorical_cols)

    import itertools

    missing_cols = set(data_encoded.columns) - set(encoded_real_time_input.columns)
    values_cycle = itertools.cycle(real_input_others)
    missing_cols_sorted = sorted(missing_cols)
    for col in missing_cols_sorted:
        value = next(values_cycle)
        encoded_real_time_input[col] = value
    encoded_real_time_input = encoded_real_time_input[X.columns]
    prediction = classifier.predict(encoded_real_time_input)
    predicted_label = label_encoder.inverse_transform(prediction)
    print("\nPredicted Label:", predicted_label[0])
    return predicted_label


def algorithm3(input_data):
    with open('naive_bias.pkl', 'rb') as file:
        classifier = pickle.load(file)
        label_encoder = pickle.load(file)
        onehot_encoder = pickle.load(file)
        categorical_cols = pickle.load(file)
        data_encoded=pickle.load(file)
        X=pickle.load(file)


    real_input = [input_data[:3]]
    real_input_others = input_data[3:]


    real_time_input_df = pd.DataFrame(real_input, columns=categorical_cols)
    encoded_real_time_input = pd.DataFrame(onehot_encoder.transform(real_time_input_df))
    encoded_real_time_input.columns = onehot_encoder.get_feature_names_out(categorical_cols)

    import itertools
    missing_cols = set(data_encoded.columns) - set(encoded_real_time_input.columns)
    values_cycle = itertools.cycle(real_input_others)
    missing_cols_sorted = sorted(missing_cols)
    for col in missing_cols_sorted:
        value = next(values_cycle)
        encoded_real_time_input[col] = value
    encoded_real_time_input = encoded_real_time_input[X.columns]
    prediction = classifier.predict(encoded_real_time_input)
    predicted_label = label_encoder.inverse_transform(prediction)
    print("\nPredicted Label:", predicted_label[0])
    return predicted_label



def algorithm4(input_data):
    with open('random_forest.pkl', 'rb') as file:
        classifier = pickle.load(file)
        label_encoder = pickle.load(file)
        onehot_encoder = pickle.load(file)
        categorical_cols = pickle.load(file)
        data_encoded=pickle.load(file)
        X=pickle.load(file)


    real_input = [input_data[:3]]
    real_input_others =input_data[3:]


    real_time_input_df = pd.DataFrame(real_input, columns=categorical_cols)
    encoded_real_time_input = pd.DataFrame(onehot_encoder.transform(real_time_input_df))
    encoded_real_time_input.columns = onehot_encoder.get_feature_names_out(categorical_cols)

    import itertools

    missing_cols = set(data_encoded.columns) - set(encoded_real_time_input.columns)
    values_cycle = itertools.cycle(real_input_others)
    missing_cols_sorted = sorted(missing_cols)
    for col in missing_cols_sorted:
        value = next(values_cycle)
        encoded_real_time_input[col] = value

    encoded_real_time_input = encoded_real_time_input[X.columns]
    prediction = classifier.predict(encoded_real_time_input)
    predicted_label = label_encoder.inverse_transform(prediction)
    print("\nPredicted Label:", predicted_label[0],"\n")
    return predicted_label



def run_algorithm(pair, input_data):
    if pair == 1:
        return algorithm1(input_data)
    elif pair == 2:
        return algorithm2(input_data)
    elif pair == 3:
        return algorithm3(input_data)
    elif pair == 4:
        return algorithm4(input_data)
    

if __name__ == "__main__":
    input_data = ['tcp', 'http', 'SF','1','146', '1','19', '11' , '1']  

    # Create a multiprocessing pool with 2 processes
    with multiprocessing.Pool(processes=2) as pool:
        # Run algorithms 1 and 2 in parallel
        results_pair1 = pool.starmap(run_algorithm, [(1, input_data), (2, input_data)])

        # Run algorithms 3 and 4 in parallel
        results_pair2 = pool.starmap(run_algorithm, [(3, input_data), (4, input_data)])

    all_results = results_pair1 + results_pair2
    normal_list = [item[0] for item in all_results]

    best_prediction = Counter(normal_list).most_common(1)[0][0]
    print("Final Prediction: ", best_prediction)





    