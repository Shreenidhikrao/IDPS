import multiprocessing
from collections import Counter
import pandas as pd
import pickle
import socket


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
    
def receive_packet_results(client_socket):
    packet_results = []
    try:
        while True:
            # Receive packet result from the socket
            data = client_socket.recv(1024)
            if not data:
                break
            # Assuming the data received is in a serialized format (e.g., JSON)
            packet_result = deserialize(data)
            packet_results.append(packet_result)
    except KeyboardInterrupt:
        pass
    return packet_results

def deserialize(data):
    # Implement your deserialization logic here
    # For simplicity, assuming data is in JSON format
    return json.loads(data)

def main():
    # Set the host and port for socket communication
    host = '127.0.0.1'
    port = 12346

    with socket.create_connection((host, port)) as client_socket:
        try:
            while True:
                # Receive and process real-time packet results
                packet_results = receive_packet_results(client_socket)

                with multiprocessing.Pool(processes=2) as pool:
                    # Process packet results using your existing algorithms
                    results_pair1 = pool.starmap(run_algorithm, [(1, packet_results), (2, packet_results)])
                    results_pair2 = pool.starmap(run_algorithm, [(3, packet_results), (4, packet_results)])

                    all_results = results_pair1 + results_pair2
                    normal_list = [item[0] for item in all_results]

                    best_prediction = Counter(normal_list).most_common(1)[0][0]
                    print("Final Prediction: ", best_prediction)

        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()





    
