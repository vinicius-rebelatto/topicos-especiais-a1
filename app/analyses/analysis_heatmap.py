import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def run_heatmap(df):
    """
    Recebe um DataFrame, seleciona colunas numéricas, calcula a correlação
    e retorna uma figura (heatmap) do matplotlib.
    """

    # 1. Selecionar apenas colunas numéricas para a correlação
    df_numeric = df.select_dtypes(include=['number'])

    # 2. Calcular a matriz de correlação
    matriz_correlacao = df_numeric.corr()

    # 3. Gerar o gráfico (Heatmap)
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 9))  # Dando um pouco mais de espaço

    sns.heatmap(
        matriz_correlacao,
        annot=True,  # Mostrar os valores de correlação
        fmt='.2f',  # Formatar com 2 casas decimais
        cmap='coolwarm',  # Esquema de cores (azul-vermelho)
        ax=ax
    )

    ax.set_title('Matriz de Correlação (Heatmap) de Atributos Numéricos', fontsize=16)
    plt.tight_layout()

    # Retornar o objeto 'figure'
    return fig