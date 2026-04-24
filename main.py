import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from pandas import crosstab
def data_injection():
    df = pd.read_csv('Covid_Data.csv')
    print(df.head())
def plot_function(df, col, mapa_etiquetas, titulo, etiqueta_x):
    
    df = df.copy()  # Evitar modificar el DataFrame original
    df['Condicion'] = df[col].map(mapa_etiquetas).fillna('Desconocido')
    # Crear la columna de fallecidos de forma binaria
    df['FALLECIDO'] = df['DATE_DIED'].apply(lambda x: 'Sí' if x != '9999-99-99' else 'No')
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
        entrada = input(
            "Ingrese 'diabetes' para analizar la relación entre diabetes y fallecidos, o 'obesidad' para analizar la relación entre obesidad y fallecidos (o 'salir' para terminar): ").lower()

        # Así lo usas en Main()
        if entrada in opciones:
            plot_function(df, *opciones[entrada])
        elif entrada == 'salir':
            print("Saliendo del programa.")
            break
        else:
            print("Entrada no válida. Por favor, ingrese 'diabetes', 'obesidad' o 'salir'.")

Main()