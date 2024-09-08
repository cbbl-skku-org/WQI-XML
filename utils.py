import numpy as np
import pandas as pd


# Default parameters
wq_params = ['PO4', 'BOD5', 'DO', 'NO3', 'NO2', 'COD', 'NH4', 'Coliform', 'pH', 'WQI']
metadata = ['Year', 'Period', 'Location']


# Feature sets based on Pearson correlation matrix
SC9 = ['PO4', 'BOD5', 'DO', 'NO3', 'NO2', 'COD', 'NH4', 'Coliform', 'pH']
SC8 = ['BOD5', 'DO', 'NO3', 'NO2', 'COD', 'NH4', 'Coliform', 'pH'] # Same as RmT9
SC7 = ['DO', 'NO3', 'NO2', 'COD', 'NH4', 'Coliform', 'pH']
SC6 = ['NO3', 'NO2', 'COD', 'NH4', 'Coliform', 'pH']
SC5 = ['NO2', 'COD', 'NH4', 'Coliform', 'pH']
SC4 = ['COD', 'NH4', 'Coliform', 'pH']
SC3 = ['NH4', 'Coliform', 'pH']
SC2 = ['Coliform', 'pH']
SC1 = ['pH']


# Feature sets based on removing individual removal
RmT1 = ['PO4', 'BOD5', 'DO', 'NO3', 'NO2', 'COD', 'NH4', 'Coliform']
RmT2 = ['PO4', 'BOD5', 'DO', 'NO3', 'NO2', 'COD', 'NH4', 'pH']
RmT3 = ['PO4', 'BOD5', 'DO', 'NO3', 'NO2', 'COD', 'Coliform', 'pH']
RmT4 = ['PO4', 'BOD5', 'DO', 'NO3', 'NO2', 'NH4', 'Coliform', 'pH']
RmT5 = ['PO4', 'BOD5', 'DO', 'NO3', 'COD', 'NH4', 'Coliform', 'pH']
RmT6 = ['PO4', 'BOD5', 'DO', 'NO2', 'COD', 'NH4', 'Coliform', 'pH']
RmT7 = ['PO4', 'BOD5', 'NO3', 'NO2', 'COD', 'NH4', 'Coliform', 'pH']
RmT8 = ['PO4', 'DO', 'NO3', 'NO2', 'COD', 'NH4', 'Coliform', 'pH']
RmT9 = ['BOD5', 'DO', 'NO3', 'NO2', 'COD', 'NH4', 'Coliform', 'pH'] # Same as SC8


# Calibrate WQI based on Vietnam's standard
# pH
BPi_pH_values = [5.5, 6, 8.5, 9]
qi_pH_values = [50, 100, 100, 50]
# DO
BPi_DO_values = [20, 50, 75, 88, 112, 125, 150, 200]
qi_DO_values = [25, 50, 75, 100, 75, 50, 25]
# COD
BPi_COD_values = [10, 15, 30, 50, 150]
qi_COD_values = [100, 75, 50, 25, 10]
# BOD5
BPi_BOD_values = [4, 6, 15, 25, 50]
qi_BOD_values = [100, 75, 50, 25, 10]
# PO4
BPi_PO4_values = [0.1, 0.2, 0.3, 0.5, 4]
qi_PO4_values = [100, 75, 50, 25, 10]
# NH4
BPi_NH4_values = [0.3, 0.6, 0.9, 5]
qi_NH4_values = [75, 50, 25, 10]
# NO2
BPi_NO2_values = [0.05]
qi_NO2_values = [100, 10]
# NO3
BPi_NO3_values = [0, 2, 5, 10]
qi_NO3_values = [100, 75, 50, 25]
# Coliform
BPi_Col_values = [2500, 5000, 7500, 10000]
qi_Col_values = [100, 75, 50, 25]


def check_variable_existence(data, variable_name):
    return variable_name in data.columns


def calculate_WQI_pH(pH_values):
    WQI_pH_values = []

    for pH_value in pH_values:
        if pH_value < BPi_pH_values[0] or pH_value > BPi_pH_values[3]:
            WQI_pH = 10
        elif BPi_pH_values[0] <= pH_value < BPi_pH_values[1]:
            BPi_pH = BPi_pH_values[0]
            BPi_plus_1_pH = BPi_pH_values[1]
            qi_pH = qi_pH_values[0]
            qi_plus_1_pH = qi_pH_values[1]
            WQI_pH = ((qi_plus_1_pH - qi_pH) / (BPi_plus_1_pH - BPi_pH)) * (pH_value - BPi_pH) + qi_pH
        elif BPi_pH_values[1] <= pH_value <= BPi_pH_values[2]:
            WQI_pH = 100
        elif BPi_pH_values[2] < pH_value <= BPi_pH_values[3]:
            BPi_pH = BPi_pH_values[2]
            BPi_plus_1_pH = BPi_pH_values[3]
            qi_pH = qi_pH_values[2]
            qi_plus_1_pH = qi_pH_values[3]
            WQI_pH = ((qi_pH - qi_plus_1_pH) / (BPi_plus_1_pH - BPi_pH)) * (BPi_plus_1_pH - pH_value) + qi_plus_1_pH
        WQI_pH_values.append(WQI_pH)

    return WQI_pH_values


def calculate_WQI_DO(DO_percent, BPi_DO_values, qi_DO_values):
    WQI_DO_values = []

    for DO_value in DO_percent:
        if DO_value <= 20 or DO_value >= 200:
            WQI_DO = 10
        elif 20 < DO_value < 50:
            BPi_DO = BPi_DO_values[0]
            BPi_plus_1_DO = BPi_DO_values[1]
            qi_DO = qi_DO_values[0]
            qi_plus_1_DO = qi_DO_values[1]
            WQI_DO = ((qi_plus_1_DO - qi_DO) / (BPi_plus_1_DO - BPi_DO)) * (DO_value - BPi_DO) + qi_DO
        elif 50 <= DO_value < 75:
            BPi_DO = BPi_DO_values[1]
            BPi_plus_1_DO = BPi_DO_values[2]
            qi_DO = qi_DO_values[1]
            qi_plus_1_DO = qi_DO_values[2]
            WQI_DO = ((qi_plus_1_DO - qi_DO) / (BPi_plus_1_DO - BPi_DO)) * (DO_value - BPi_DO) + qi_DO
        elif 75 <= DO_value < 88:
            BPi_DO = BPi_DO_values[2]
            BPi_plus_1_DO = BPi_DO_values[3]
            qi_DO = qi_DO_values[2]
            qi_plus_1_DO = qi_DO_values[3]
            WQI_DO = ((qi_plus_1_DO - qi_DO) / (BPi_plus_1_DO - BPi_DO)) * (DO_value - BPi_DO) + qi_DO
        elif 88 <= DO_value <= 112:
            WQI_DO = 100
        elif 112 < DO_value < 125:
            BPi_DO = BPi_DO_values[3]
            BPi_plus_1_DO = BPi_DO_values[4]
            qi_DO = qi_DO_values[3]
            qi_plus_1_DO = qi_DO_values[4]
            WQI_DO = ((qi_DO - qi_plus_1_DO) / (BPi_plus_1_DO - BPi_DO)) * (BPi_plus_1_DO - DO_value) + qi_plus_1_DO
        elif 125 <= DO_value < 150:
            BPi_DO = BPi_DO_values[4]
            BPi_plus_1_DO = BPi_DO_values[5]
            qi_DO = qi_DO_values[4]
            qi_plus_1_DO = qi_DO_values[5]
            WQI_DO = ((qi_DO - qi_plus_1_DO) / (BPi_plus_1_DO - BPi_DO)) * (BPi_plus_1_DO - DO_value) + qi_plus_1_DO
        elif 150 <= DO_value < 200:
            BPi_DO = BPi_DO_values[5]
            BPi_plus_1_DO = BPi_DO_values[6]
            qi_DO = qi_DO_values[5]
            qi_plus_1_DO = qi_DO_values[6]
            WQI_DO = ((qi_DO - qi_plus_1_DO) / (BPi_plus_1_DO - BPi_DO)) * (BPi_plus_1_DO - DO_value) + qi_plus_1_DO
        WQI_DO_values.append(WQI_DO)

    return WQI_DO_values


def calculate_WQI_COD(COD_values):
    WQI_COD_values = []

    for COD_value in COD_values:
        if COD_value <= BPi_COD_values[0]:
            WQI_COD = 100
        elif BPi_COD_values[0] < COD_value < BPi_COD_values[1]:
            BPi_COD = BPi_COD_values[0]
            BPi_plus_1_COD = BPi_COD_values[1]
            qi_COD = qi_COD_values[0]
            qi_plus_1_COD = qi_COD_values[1]
            WQI_COD = ((qi_COD - qi_plus_1_COD) / (BPi_plus_1_COD - BPi_COD)) * (
                        BPi_plus_1_COD - COD_value) + qi_plus_1_COD
        elif BPi_COD_values[1] <= COD_value < BPi_COD_values[2]:
            BPi_COD = BPi_COD_values[1]
            BPi_plus_1_COD = BPi_COD_values[2]
            qi_COD = qi_COD_values[1]
            qi_plus_1_COD = qi_COD_values[2]
            WQI_COD = ((qi_COD - qi_plus_1_COD) / (BPi_plus_1_COD - BPi_COD)) * (
                        BPi_plus_1_COD - COD_value) + qi_plus_1_COD
        elif BPi_COD_values[2] <= COD_value < BPi_COD_values[3]:
            BPi_COD = BPi_COD_values[2]
            BPi_plus_1_COD = BPi_COD_values[3]
            qi_COD = qi_COD_values[2]
            qi_plus_1_COD = qi_COD_values[3]
            WQI_COD = ((qi_COD - qi_plus_1_COD) / (BPi_plus_1_COD - BPi_COD)) * (
                        BPi_plus_1_COD - COD_value) + qi_plus_1_COD
        elif BPi_COD_values[3] <= COD_value < BPi_COD_values[4]:
            BPi_COD = BPi_COD_values[3]
            BPi_plus_1_COD = BPi_COD_values[4]
            qi_COD = qi_COD_values[3]
            qi_plus_1_COD = qi_COD_values[4]
            WQI_COD = ((qi_COD - qi_plus_1_COD) / (BPi_plus_1_COD - BPi_COD)) * (
                        BPi_plus_1_COD - COD_value) + qi_plus_1_COD
        else:
            WQI_COD = 10

        WQI_COD_values.append(WQI_COD)

    return WQI_COD_values


def calculate_WQI_BOD(BOD_values, BPi_BOD_values, qi_BOD_values):
    WQI_BOD_values = []

    for BOD_value in BOD_values:
        if BOD_value <= BPi_BOD_values[0]:
            WQI_BOD = 100
        elif BPi_BOD_values[0] < BOD_value < BPi_BOD_values[1]:
            BPi_BOD = BPi_BOD_values[0]
            BPi_plus_1_BOD = BPi_BOD_values[1]
            qi_BOD = qi_BOD_values[0]
            qi_plus_1_BOD = qi_BOD_values[1]
            WQI_BOD = ((qi_BOD - qi_plus_1_BOD) / (BPi_plus_1_BOD - BPi_BOD)) * (
                        BPi_plus_1_BOD - BOD_value) + qi_plus_1_BOD
        elif BPi_BOD_values[1] <= BOD_value < BPi_BOD_values[2]:
            BPi_BOD = BPi_BOD_values[1]
            BPi_plus_1_BOD = BPi_BOD_values[2]
            qi_BOD = qi_BOD_values[1]
            qi_plus_1_BOD = qi_BOD_values[2]
            WQI_BOD = ((qi_BOD - qi_plus_1_BOD) / (BPi_plus_1_BOD - BPi_BOD)) * (
                        BPi_plus_1_BOD - BOD_value) + qi_plus_1_BOD
        elif BPi_BOD_values[2] <= BOD_value < BPi_BOD_values[3]:
            BPi_BOD = BPi_BOD_values[2]
            BPi_plus_1_BOD = BPi_BOD_values[3]
            qi_BOD = qi_BOD_values[2]
            qi_plus_1_BOD = qi_BOD_values[3]
            WQI_BOD = ((qi_BOD - qi_plus_1_BOD) / (BPi_plus_1_BOD - BPi_BOD)) * (
                        BPi_plus_1_BOD - BOD_value) + qi_plus_1_BOD
        elif BPi_BOD_values[3] <= BOD_value < BPi_BOD_values[4]:
            BPi_BOD = BPi_BOD_values[3]
            BPi_plus_1_BOD = BPi_BOD_values[4]
            qi_BOD = qi_BOD_values[3]
            qi_plus_1_BOD = qi_BOD_values[4]
            WQI_BOD = ((qi_BOD - qi_plus_1_BOD) / (BPi_plus_1_BOD - BPi_BOD)) * (
                        BPi_plus_1_BOD - BOD_value) + qi_plus_1_BOD
        else:
            WQI_BOD = 10

        WQI_BOD_values.append(WQI_BOD)

    return WQI_BOD_values


def calculate_WQI_PO4(PO4_values):
    WQI_PO4_values = []

    for PO4_value in PO4_values:
        if PO4_value is not None:  # Check if PO4_value exists and is not None
            if PO4_value <= BPi_PO4_values[0]:
                WQI_PO4 = 100
            elif BPi_PO4_values[0] < PO4_value < BPi_PO4_values[1]:
                BPi_PO4 = BPi_PO4_values[0]
                BPi_plus_1_PO4 = BPi_PO4_values[1]
                qi_PO4 = qi_PO4_values[0]
                qi_plus_1_PO4 = qi_PO4_values[1]
                WQI_PO4 = ((qi_PO4 - qi_plus_1_PO4) / (BPi_plus_1_PO4 - BPi_PO4)) * (BPi_plus_1_PO4 - PO4_value) + qi_plus_1_PO4
            elif BPi_PO4_values[1] <= PO4_value < BPi_PO4_values[2]:
                BPi_PO4 = BPi_PO4_values[1]
                BPi_plus_1_PO4 = BPi_PO4_values[2]
                qi_PO4 = qi_PO4_values[1]
                qi_plus_1_PO4 = qi_PO4_values[2]
                WQI_PO4 = ((qi_PO4 - qi_plus_1_PO4) / (BPi_plus_1_PO4 - BPi_PO4)) * (BPi_plus_1_PO4 - PO4_value) + qi_plus_1_PO4
            elif BPi_PO4_values[2] <= PO4_value < BPi_PO4_values[3]:
                BPi_PO4 = BPi_PO4_values[2]
                BPi_plus_1_PO4 = BPi_PO4_values[3]
                qi_PO4 = qi_PO4_values[2]
                qi_plus_1_PO4 = qi_PO4_values[3]
                WQI_PO4 = ((qi_PO4 - qi_plus_1_PO4) / (BPi_plus_1_PO4 - BPi_PO4)) * (BPi_plus_1_PO4 - PO4_value) + qi_plus_1_PO4
            elif BPi_PO4_values[3] <= PO4_value < BPi_PO4_values[4]:
                BPi_PO4 = BPi_PO4_values[3]
                BPi_plus_1_PO4 = BPi_PO4_values[4]
                qi_PO4 = qi_PO4_values[3]
                qi_plus_1_PO4 = qi_PO4_values[4]
                WQI_PO4 = ((qi_PO4 - qi_plus_1_PO4) / (BPi_plus_1_PO4 - BPi_PO4)) * (BPi_plus_1_PO4 - PO4_value) + qi_plus_1_PO4
            else:
                WQI_PO4 = 10  # Out of range value

        else:
            WQI_PO4 = None  # PO4_value is None

        WQI_PO4_values.append(WQI_PO4)

    return WQI_PO4_values


def calculate_WQI_NH4(NH4_values):
    WQI_NH4_values = []

    for NH4_value in NH4_values:
        if NH4_value is not None:  # Check if NH4_value exists
            if NH4_value < BPi_NH4_values[0]:
                WQI_NH4 = 100
            elif BPi_NH4_values[0] <= NH4_value < BPi_NH4_values[1]:
                BPi_NH4 = BPi_NH4_values[0]
                BPi_plus_1_NH4 = BPi_NH4_values[1]
                qi_NH4 = qi_NH4_values[0]
                qi_plus_1_NH4 = qi_NH4_values[1]
                WQI_NH4 = ((qi_NH4 - qi_plus_1_NH4) / (BPi_plus_1_NH4 - BPi_NH4)) * (BPi_plus_1_NH4 - NH4_value) + qi_plus_1_NH4
            elif BPi_NH4_values[1] <= NH4_value < BPi_NH4_values[2]:
                BPi_NH4 = BPi_NH4_values[1]
                BPi_plus_1_NH4 = BPi_NH4_values[2]
                qi_NH4 = qi_NH4_values[1]
                qi_plus_1_NH4 = qi_NH4_values[2]
                WQI_NH4 = ((qi_NH4 - qi_plus_1_NH4) / (BPi_plus_1_NH4 - BPi_NH4)) * (BPi_plus_1_NH4 - NH4_value) + qi_plus_1_NH4
            elif BPi_NH4_values[2] <= NH4_value < BPi_NH4_values[3]:
                BPi_NH4 = BPi_NH4_values[2]
                BPi_plus_1_NH4 = BPi_NH4_values[3]
                qi_NH4 = qi_NH4_values[2]
                qi_plus_1_NH4 = qi_NH4_values[3]
                WQI_NH4 = ((qi_NH4 - qi_plus_1_NH4) / (BPi_plus_1_NH4 - BPi_NH4)) * (BPi_plus_1_NH4 - NH4_value) + qi_plus_1_NH4
            else:
                WQI_NH4 = 10
        else:
            WQI_NH4 = None  # NH4_value does not exist

        WQI_NH4_values.append(WQI_NH4)

    return WQI_NH4_values


def calculate_WQI_NO2(NO2_values):
    WQI_NO2_values = []

    for NO2_value in NO2_values:
        if NO2_value is not None:  # Check if NO2_value exists
            if NO2_value <= BPi_NO2_values[0]:
                WQI_NO2 = qi_NO2_values[0]
            else:
                WQI_NO2 = qi_NO2_values[1]
        else:
            WQI_NO2 = None  # NO2_value does not exist

        WQI_NO2_values.append(WQI_NO2)

    return WQI_NO2_values


def calculate_WQI_NO3(NO3_values):
    WQI_NO3_values = []

    for NO3_value in NO3_values:
        if NO3_value is not None:
            if NO3_value <= 2:
                WQI_NO3 = 100
            elif 2 < NO3_value < 5:
                BPi_NO3 = BPi_NO3_values[1]
                BPi_plus_1_NO3 = BPi_NO3_values[2]
                qi_NO3 = qi_NO3_values[0]
                qi_plus_1_NO3 = qi_NO3_values[1]
                WQI_NO3 = ((qi_NO3 - qi_plus_1_NO3) / (BPi_plus_1_NO3 - BPi_NO3)) * (BPi_plus_1_NO3 - NO3_value) + qi_plus_1_NO3
            elif 5 <= NO3_value < 10:
                BPi_NO3 = BPi_NO3_values[2]
                BPi_plus_1_NO3 = BPi_NO3_values[3]
                qi_NO3 = qi_NO3_values[1]
                qi_plus_1_NO3 = qi_NO3_values[2]
                WQI_NO3 = ((qi_NO3 - qi_plus_1_NO3) / (BPi_plus_1_NO3 - BPi_NO3)) * (BPi_plus_1_NO3 - NO3_value) + qi_plus_1_NO3
            elif 10 <= NO3_value <= 15:
                BPi_NO3 = BPi_NO3_values[3]
                BPi_plus_1_NO3 = 15
                qi_NO3 = qi_NO3_values[2]
                qi_plus_1_NO3 = 10
                WQI_NO3 = ((qi_NO3 - qi_plus_1_NO3) / (BPi_plus_1_NO3 - BPi_NO3)) * (BPi_plus_1_NO3 - NO3_value) + qi_plus_1_NO3
            else:
                WQI_NO3 = 10
        else:
            WQI_NO3 = None

        WQI_NO3_values.append(WQI_NO3)

    return WQI_NO3_values


def calculate_WQI_Col(Coliform_values):
    WQI_Col_values = []

    for Col_value in Coliform_values:
        if Col_value is not None:
            if Col_value <= BPi_Col_values[0]:
                WQI_Col = 100

            elif BPi_Col_values[0] < Col_value < BPi_Col_values[1]:
                BPi_Col = BPi_Col_values[0]
                qi_Col = qi_Col_values[0]
                qi_plus_1_Col = qi_Col_values[1]
                WQI_Col = ((qi_Col - qi_plus_1_Col) / (BPi_Col_values[1] - BPi_Col)) * (BPi_Col_values[1] - Col_value) + qi_plus_1_Col

            elif BPi_Col_values[1] <= Col_value < BPi_Col_values[2]:
                BPi_Col = BPi_Col_values[1]
                qi_Col = qi_Col_values[1]
                qi_plus_1_Col = qi_Col_values[2]
                WQI_Col = ((qi_Col - qi_plus_1_Col) / (BPi_Col_values[2] - BPi_Col)) * (BPi_Col_values[2] - Col_value) + qi_plus_1_Col

            elif BPi_Col_values[2] <= Col_value < BPi_Col_values[3]:
                BPi_Col = BPi_Col_values[2]
                qi_Col = qi_Col_values[2]
                qi_plus_1_Col = qi_Col_values[3]
                WQI_Col = ((qi_Col - qi_plus_1_Col) / (BPi_Col_values[3] - BPi_Col)) * (BPi_Col_values[3] - Col_value) + qi_plus_1_Col

            else:
                WQI_Col = 10

        else:
            WQI_Col = None

        WQI_Col_values.append(WQI_Col)

    return WQI_Col_values


def VN_WQI_Calculation(original_data_path):
    VN_WQI = []
    data = pd.DataFrame()
    non_Vietnamese_standard_data = pd.read_csv(original_data_path)
    if check_variable_existence(non_Vietnamese_standard_data, 'pH'):
        pH_values = non_Vietnamese_standard_data['pH']
        WQI_pH_values = calculate_WQI_pH(pH_values)
        data['WQI_pH'] = WQI_pH_values
    else:
        print("Variable 'pH' does not exist in DataFrame. Skip calculating WQI_pH")
    if check_variable_existence(non_Vietnamese_standard_data, 'COD'):
        COD_values = non_Vietnamese_standard_data['COD']
        WQI_COD_values = calculate_WQI_COD(COD_values)
        data['WQI_COD'] = WQI_COD_values
    else:
        print("Variable 'COD' does not exist in DataFrame. Skip calculating WQI_COD")
    if check_variable_existence(non_Vietnamese_standard_data, 'BOD5'):
        BOD_values = non_Vietnamese_standard_data['BOD5']
        WQI_BOD_values = calculate_WQI_BOD(BOD_values, BPi_BOD_values, qi_BOD_values)
        data['WQI_BOD'] = WQI_BOD_values
    else:
        print("Variable 'BOD5' does not exist in DataFrame. Skipping WQI_BOD calculation.")
    if check_variable_existence(non_Vietnamese_standard_data, 'PO4'):
        WQI_PO4_values = calculate_WQI_PO4(non_Vietnamese_standard_data['PO4'])
        data['WQI_PO4'] = WQI_PO4_values
    else:
        print("The variable 'PO4' does not exist in the DataFrame. Aborting calculation of WQI_PO4")
    if check_variable_existence(non_Vietnamese_standard_data, 'NH4'):
        WQI_NH4_values = calculate_WQI_PO4(non_Vietnamese_standard_data['NH4'])
        data['WQI_NH4'] = WQI_NH4_values
    else:
        print("The variable 'NH4' does not exist in the DataFrame. Aborting calculation of WQI_NH4")
    if check_variable_existence(non_Vietnamese_standard_data, 'NO2'):
        WQI_NO2_values = calculate_WQI_NO2(non_Vietnamese_standard_data['NO2'])
        data['WQI_NO2'] = WQI_NO2_values
    else:
        print("The variable 'NO2' does not exist in the DataFrame. Skip calculating WQI_NO2.")
    if check_variable_existence(non_Vietnamese_standard_data, 'NO3'):
        NO3_values = non_Vietnamese_standard_data['NO3']
        WQI_NO3_values = calculate_WQI_NO3(NO3_values)
        data['WQI_NO3'] = WQI_NO3_values
    else:
        print("Variable 'NO3' does not exist in the DataFrame. Skip calculating WQI_NO3.")
    if check_variable_existence(non_Vietnamese_standard_data, 'Coliform'):
        Coliform_values = non_Vietnamese_standard_data['Coliform']
        WQI_Col_values = calculate_WQI_Col(Coliform_values)
        data['WQI_Col'] = WQI_Col_values
    else:
        print("Variable 'Coliform' does not exist in the DataFrame. Skip calculating WQI_Col.")
    for _, row in data.iterrows():
        # Check the existence of variables and assign values if any
        pH = row['WQI_pH'] if 'WQI_pH' in row else None
        DO = row['WQI_DO'] if 'WQI_DO' in row else None
        BOD5 = row['WQI_BOD'] if 'WQI_BOD' in row else None
        COD = row['WQI_COD'] if 'WQI_COD' in row else None
        NH4 = row['WQI_NH4'] if 'WQI_NH4' in row else None
        NO3 = row['WQI_NO3'] if 'WQI_NO3' in row else None
        NO2 = row['WQI_NO2'] if 'WQI_NO2' in row else None
        PO4 = row['WQI_PO4'] if 'WQI_PO4' in row else None
        Col = row['WQI_Col'] if 'WQI_Col' in row else None

        # Create a list of available values (not None)
        values = [val for val in [DO, BOD5, COD, NH4, NO3, NO2, PO4] if val is not None]

        # If there is no value, skip this line
        if len(values) == 0:
            VN_WQI.append(None)
            continue

        # Calculate individual WQI components if sufficient data is available
        WQI_1 = pH / 100 if pH is not None else 1  # Default value if pH is not available
        WQI_4 = (sum(values) / len(values)) ** 2
        WQI_5 = Col if Col is not None else 1  # Default value if Colìorm is not present

        # Calculate total WQI using the formula provided
        WQI = round(WQI_1 * (WQI_4 * WQI_5) ** (1 / 3), 2)
        VN_WQI.append(WQI)
        
    return VN_WQI