import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from pandas import crosstab
def plot_diabetes():
    df = pd.read_csv('Covid_Data.csv')

    df['DIABETES_CLEAN'] = df['DIABETES'].map({1:'Con Diabetes',2:'Sin Diabetes'}).fillna('Desconocido')
    # Crear la columna de fallecidos de forma binaria
    df['FALLECIDO'] = df['DATE_DIED'].apply(lambda x: 'Sí' if x != '9999-99-99' else 'No')
    crosstab = pd.crosstab(df['DIABETES_CLEAN'],df['FALLECIDO'], normalize="index")

    crosstab.plot(
        kind = 'bar',
        figsize = (8,5),
        color = ['steelblue','tomato'],
        edgecolor = 'white'
    )
    plt.title('Diabetes vs Fallecidos por Covid-19')
    plt.xlabel('Categoria de Diabetes')
    plt.ylabel('Numero de Pacientes')
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    plt.xticks(rotation = 0)
    plt.legend(labels=['Sobrevivió', 'Falleció'],
        title='Estado del Paciente',
        loc='upper right')
    plt.tight_layout()
    plt.show()
def plot_obesidad():
    df = pd.read_csv('Covid_Data.csv')

    df['OBESIDAD_CLEAN'] = df['OBESITY'].map({1: 'Con Obesidad', 2: 'Sin Obesidad'}).fillna('Desconocido')
    # Crear la columna de fallecidos de forma binaria
    df['FALLECIDO'] = df['DATE_DIED'].apply(lambda x: 'Sí' if x != '9999-99-99' else 'No')
    crosstab = pd.crosstab(df['OBESIDAD_CLEAN'], df['FALLECIDO'], normalize="index")

    crosstab.plot(
        kind='bar',
        figsize=(8, 5),
        color=['steelblue', 'tomato'],
        edgecolor='white'
    )
    plt.title('Obesidad vs Fallecidos por Covid-19')
    plt.xlabel('Categoria de Obesidad')
    plt.ylabel('Numero de Pacientes')
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    plt.xticks(rotation=0)
    plt.legend(labels=['Sobrevivió', 'Falleció'],
               title='Estado del Paciente',
               loc='upper right')
    plt.tight_layout()
    plt.show()

def Main():
    while True:
        input_usuario = input('Diga que plot desea: ').lower()
        dict = {'obesidad':plot_obesidad,'diabetes':plot_diabetes}
        if input_usuario in dict.keys():
            dict[input_usuario]()
        elif input_usuario.lower() == 'salir':
            print('Saliendo del programa........')
            break
        else:
            print('error no plot para estas opciones...')


Main()