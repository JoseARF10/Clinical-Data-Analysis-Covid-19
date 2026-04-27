import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pandas import crosstab
import sqlite3

def get_column_names(df):
    df = df.copy()
    for col in df.columns:
        print(f'Column: {col}')

def data_injection(df):
    try:
        with sqlite3.connect('patients.db') as conn:
            df = df.copy()
            mappings = {
                'USMER': {1: 'First Level', 2: 'Second Level', 3: 'Third Level'},
                'SEX': {1: 'Female', 2: 'Male'},
                'PATIENT_TYPE': {1: 'Outpatient', 2: 'Hospitalized'},
                'INTUBED': {1: 'Yes', 2: 'No', 97: 'Not Applicable', 98: 'Unknown', 99: 'Not Specified'},
                'PNEUMONIA': {1: 'Yes', 2: 'No', 97: 'Not Applicable', 98: 'Unknown', 99: 'Not Specified'},
                'PREGNANT': {1: 'Yes', 2: 'No', 97: 'Not Applicable', 98: 'Unknown', 99: 'Not Specified'},
                'DIABETES': {1: 'Yes', 2: 'No', 98: 'Unknown', 99: 'Not Specified'},
                'COPD': {1: 'Yes', 2: 'No', 98: 'Unknown', 99: 'Not Specified'},
                'ASTHMA': {1: 'Yes', 2: 'No', 98: 'Unknown', 99: 'Not Specified'},
                'INMSUPR': {1: 'Yes', 2: 'No', 98: 'Unknown', 99: 'Not Specified'},
                'HIPERTENSION': {1: 'Yes', 2: 'No', 98: 'Unknown', 99: 'Not Specified'},
                'OTHER_DISEASE': {1: 'Yes', 2: 'No', 98: 'Unknown', 99: 'Not Specified'},
                'CARDIOVASCULAR': {1: 'Yes', 2: 'No', 98: 'Unknown', 99: 'Not Specified'},
                'OBESITY': {1: 'Yes', 2: 'No', 98: 'Unknown', 99: 'Not Specified'},
                'RENAL_CHRONIC': {1: 'Yes', 2: 'No', 98: 'Unknown', 99: 'Not Specified'},
                'TOBACCO': {1: 'Yes', 2: 'No', 98: 'Unknown', 99: 'Not Specified'},
                'ICU': {1: 'Yes', 2: 'No', 97: 'Not Applicable', 98: 'Unknown', 99: 'Not Specified'},
            }
            for col, mapping in mappings.items():
                if col in df.columns:
                    df[col] = df[col].replace(mapping)
            df['DATE_DIED'] = pd.to_datetime(df['DATE_DIED'], errors='coerce', dayfirst=True)
            df['DATE_DIED'] = df['DATE_DIED'].dt.strftime('%Y-%m-%d').fillna('Alive')
            df.to_sql('patient_information', conn, if_exists='replace', index=False, chunksize=1000)
            print("Data cleaned and inserted successfully into the SQLite database.")
    except Exception as e:
        print(f"Error cleaning and inserting data: {e}")

def plot_function(df, col, label_map, title, x_label):
    df = df.copy()
    df['Condition'] = df[col].map(label_map).fillna('Unknown')
    df['DECEASED'] = df['DATE_DIED'].apply(lambda x: 'Yes' if str(x) != '9999-99-99' else 'No')
    crosstab = pd.crosstab(df['Condition'], df['DECEASED'], normalize="index")
    crosstab.plot(
        kind='bar',
        figsize=(8, 5),
        color=['steelblue', 'tomato'],
        edgecolor='white'
    )
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel('Number of Patients')
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    plt.xticks(rotation=0)
    plt.legend(labels=['Survived', 'Deceased'], title='Patient Status', loc='upper right')
    plt.tight_layout()
    plt.show()

def main():
    while True:
        file_name = input("Type the name of the file (with .csv extension): ")
        try:
            open(file_name, 'r').close()
            df = pd.read_csv(file_name, encoding='utf-8')
            break
        except FileNotFoundError:
            print("File not found. Please try again.\n")

    options = {
        'diabetes': ('DIABETES', {1: 'With Diabetes', 2: 'Without Diabetes'}, 'Diabetes vs Deceased', 'Category'),
        'obesity': ('OBESITY', {1: 'With Obesity', 2: 'Without Obesity'}, 'Obesity vs Deceased', 'Category'),
    }

    while True:
        print("\n=== COVID-19 MEXICO ANALYSIS ===")
        print("  diabetes          → Relationship between diabetes and deaths")
        print("  obesity           → Relationship between obesity and deaths")
        print("  obesity diabetes  → Relationship between obesity & diabetes and deaths")
        print("  data-cleaning     → Clean and save data to SQLite")
        print("  exit              → Quit")
        print("=" * 32)

        entry = input("Enter command: ").lower()

        if entry in options:
            plot_function(df, *options[entry])
        elif entry == 'data-cleaning':
            data_injection(df)
        elif entry == 'obesity diabetes':
            df_temp = df.copy()
            df_temp['Condition'] = df_temp.apply(
                lambda row: 'Obesity and Diabetes' if row['OBESITY'] == 1 and row['DIABETES'] == 1
                else 'Without Obesity and Diabetes', axis=1
            )
            plot_function(df_temp, 'Condition',
                          {'Obesity and Diabetes': 'Obesity and Diabetes',
                           'Without Obesity and Diabetes': 'Without Obesity and Diabetes'},
                          'Obesity and Diabetes vs Deceased', 'Category')
        elif entry == 'exit':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please enter 'diabetes', 'obesity', 'obesity diabetes', 'data-cleaning', or 'exit'.")

main()