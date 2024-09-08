import numpy as np
import pandas as pd
import pickle
import argparse
from utils import *
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import math

def load_data(data_path, scaler_path):
    data = pd.read_csv(data_path)
    original_headers_list = data.columns.tolist()
    print(original_headers_list)
    for col in original_headers_list:
        if col in metadata:
            data = data.drop([col], axis=1)
        elif col not in wq_params:
            data = data.drop([col], axis=1)
            print("{} is not included in WQ parameters!!!".format(col))
    if 'WQI' in original_headers_list:
        features = data.drop(['WQI'], axis=1)
        preprocessed_headers_list = features
        features = np.array(features).astype(np.float32)
        labels = data['WQI']
        labels = np.array(labels).astype(np.float32)
    else:
        features = data
        preprocessed_headers_list = features
        features = np.array(features).astype(np.float32)
        labels = None
    if set(preprocessed_headers_list) == set(SC9):
        feature_set = 'full'
    elif set(preprocessed_headers_list) == set(SC8) or set(preprocessed_headers_list) == set(RmT9):
        feature_set = 'SC8'
    elif set(preprocessed_headers_list) == set(SC7):
        feature_set = 'SC7'
    elif set(preprocessed_headers_list) == set(SC6):
        feature_set = 'SC6'
    elif set(preprocessed_headers_list) == set(SC5):
        feature_set = 'SC5'
    elif set(preprocessed_headers_list) == set(SC4):
        feature_set = 'SC4'
    elif set(preprocessed_headers_list) == set(SC3):
        feature_set = 'SC3'
    elif set(preprocessed_headers_list) == set(SC2):
        feature_set = 'SC2'
    elif set(preprocessed_headers_list) == set(RmT3):
        feature_set = 'RmT3'
    elif set(preprocessed_headers_list) == set(RmT4):
        feature_set = 'RmT4'
    elif set(preprocessed_headers_list) == set(RmT5):
        feature_set = 'RmT5'
    elif set(preprocessed_headers_list) == set(RmT6):
        feature_set = 'RmT6'
    elif set(preprocessed_headers_list) == set(RmT7):
        feature_set = 'RmT7'
    elif set(preprocessed_headers_list) == set(RmT8):
        feature_set = 'RmT8'
    scaler = pickle.load(open(scaler_path + '/scaler_weight_' + feature_set + '.pkl', 'rb'))
    features = scaler.transform(features)
    return features, labels, feature_set

def load_model(model_path, model_name, feature_set):
    model = pickle.load(open(model_path + '/' + model_name + '_' + feature_set + '.pkl', 'rb'))
    return model

def main(args):
    features, labels, feature_set = load_data(args.test_data_path, args.norm_weight_path)
    print("Data loaded!!!")
    model = load_model(args.model_path, args.model_name, feature_set)
    print("Model loaded!!!")
    results = model.predict(features)
    print("Predicted!!!")
    if args.output_path:
        if labels is not None:
            df = pd.DataFrame(zip(labels, results), columns=['WQI_true', 'WQI_pred'])
            df.to_csv(args.output_path + '/' + 'results.csv', header=True, index=None)
            rmse_value = math.sqrt(mean_squared_error(labels, results))
            print("RMSE: {:.4f}".format(rmse_value))
            mae_value = mean_absolute_error(labels, results)
            print("MAE: {:.4f}".format(mae_value))
            r_squared_value = r2_score(labels, results)
            print("R²: {:.4f}".format(r_squared_value))
        else:
            df = pd.DataFrame(results, columns=['WQI_pred'])
            df.to_csv(args.output_path + '/' + 'results.csv', header=True, index=None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='XGB', choices=['AB', 'CB', 'GB', 'LGB', 'XGB'])
    parser.add_argument('--model_path', type=str, help='Path to the saved model', required=True)
    parser.add_argument('--test_data_path', type=str, required=True)
    parser.add_argument('--norm_weight_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=False)
    args = parser.parse_args()
    main(args)
    print("Done.")