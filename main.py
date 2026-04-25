import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pandas import crosstab
import sqlite3
def get_nombre_columna(df):
    df = df.copy()  # Evitar modificar el DataFrame original
    for col in df.columns:
        print(f'Columna: {col}')
def data_injection(df):
    try:
        with sqlite3.connect('pacientes.db') as conn:
            df = df.copy()  # Evitar modificar el DataFrame original
            mappings = {
            'USMER': {1: 'Primer Nivel', 2: 'Segundo Nivel', 3: 'Tercer Nivel'},
            'SEX': {1: 'Femenino', 2: 'Masculino'},
            'PATIENT_TYPE': {1: 'Ambulatorio', 2: 'Hospitalizado'},
            'INTUBED': {1: 'Sí', 2: 'No', 97: 'No Aplica', 98: 'Se Ignora', 99: 'No Especificado'},
            'PNEUMONIA': {1: 'Sí', 2: 'No', 97: 'No Aplica', 98: 'Se Ignora', 99: 'No Especificado'},
            'PREGNANT': {1: 'Sí', 2: 'No', 97: 'No Aplica', 98: 'Se Ignora', 99: 'No Especificado'},
            'DIABETES': {1: 'Sí', 2: 'No', 98: 'Se Ignora', 99: 'No Especificado'},
            'COPD': {1: 'Sí', 2: 'No', 98: 'Se Ignora', 99: 'No Especificado'},
            'ASTHMA': {1: 'Sí', 2: 'No', 98: 'Se Ignora', 99: 'No Especificado'},
            'INMSUPR': {1: 'Sí', 2: 'No', 98: 'Se Ignora', 99: 'No Especificado'},
            'HIPERTENSION': {1: 'Sí', 2: 'No', 98: 'Se Ignora', 99: 'No Especificado'},
            'OTHER_DISEASE': {1: 'Sí', 2: 'No', 98: 'Se Ignora', 99: 'No Especificado'},
            'CARDIOVASCULAR': {1: 'Sí', 2: 'No', 98: 'Se Ignora', 99: 'No Especificado'},
            'OBESITY': {1: 'Sí', 2: 'No', 98: 'Se Ignora', 99: 'No Especificado'},
            'RENAL_CHRONIC': {1: 'Sí', 2: 'No', 98: 'Se Ignora', 99: 'No Especificado'},
            'TOBACCO': {1: 'Sí', 2: 'No', 98: 'Se Ignora', 99: 'No Especificado'},
            'ICU': {1: 'Sí', 2: 'No', 97: 'No Aplica', 98: 'Se Ignora', 99: 'No Especificado'},
            }
            # Aplicar todos los mappings de una vez
            for col, mapping in mappings.items():
                if col in df.columns:
                        df[col] = df[col].replace(mapping)  
            df['DATE_DIED'] = pd.to_datetime(df['DATE_DIED'], errors='coerce',dayfirst=True)
            df['DATE_DIED'] = df['DATE_DIED'].dt.strftime('%Y-%m-%d').fillna('Vivo')
            df.to_sql('informacion_pacientes', conn, if_exists='replace', index=False,chunksize=1000)
            print("Datos limpiados e insertados correctamente en la base de datos SQLite.")
    except Exception as e:
        print(f"Error al limpiar e insertar datos: {e}")
def plot_function(df, col, mapa_etiquetas, titulo, etiqueta_x):
    df = df.copy()  # Evitar modificar el DataFrame original
    df['Condicion'] = df[col].map(mapa_etiquetas).fillna('Desconocido')
    # Crear la columna de fallecidos de forma binaria
    df['FALLECIDO'] = df['DATE_DIED'].apply(lambda x: 'No' if str(x) != '9999-99-99' else 'Sí')
    crosstab = pd.crosstab(df['Condicion'], df['FALLECIDO'], normalize="index")
    crosstab.plot(
        kind='bar',
        figsize=(8, 5),
        color=['steelblue', 'tomato'],
        edgecolor='white'
    )
    plt.title(titulo)
    plt.xlabel(etiqueta_x)
    plt.ylabel('Numero de Pacientes')
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    plt.xticks(rotation=0)
    plt.legend(labels=['Sobrevivió', 'Falleció'],
               title='Estado del Paciente',
               loc='upper right')
    plt.tight_layout()
    plt.show()
def Main():
    df = pd.read_csv('Covid_Data.csv')
    opciones = {
            'diabetes': ('DIABETES', 
                         {1: 'Con Diabetes', 2: 'Sin Diabetes'}
                         , 'Diabetes vs Fallecidos', 'Categoría'),
            'obesidad': ('OBESITY',  
                         {1: 'Con Obesidad',  2: 'Sin Obesidad'}
                         , 'Obesidad vs Fallecidos', 'Categoría'),
            
             
                
        }
    while True:
        print("\n=== ANÁLISIS COVID-19 MÉXICO ===")
        print("  diabetes      → Relación diabetes y fallecidos")
        print("  obesidad      → Relación obesidad y fallecidos")
        print("  obesidad y diabetes → Relación obesidad y diabetes con fallecidos")
        print("  data-cleaning → Limpiar y guardar en SQLite")
        print("  salir         → Terminar")
        print("=" * 32)
        entrada = input(
        "Ingrese : "
        ).lower()
        if entrada in opciones:
            plot_function(df, *opciones[entrada])
        elif entrada =='data-cleaning':
            data_injection(df)
        elif entrada == 'obesidad y diabetes':
            df = df.copy()  # Evitar modificar el DataFrame original
            df['Condicion'] = df.apply(lambda row: 'Obesidad y Diabetes' if row['OBESITY'] == 1 and row['DIABETES'] == 1 else 'Sin Obesidad y Diabetes', axis=1)
            plot_function(df, 'Condicion', {'Obesidad y Diabetes': 'Obesidad y Diabetes', 'Sin Obesidad y Diabetes': 'Sin Obesidad y Diabetes'}, 'Obesidad y Diabetes vs Fallecidos', 'Categoría')
        elif entrada == 'salir':
            print("Saliendo del programa.")
            break
        else:
            print("Entrada no válida. Por favor, ingrese 'diabetes', 'obesidad' o 'salir'.")
Main()

