# analyses/analysis_002.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def run_analysis_002(df):
    """
    Carrega o dataset, identifica os bairros com mais anúncios e cria um
    boxplot para visualizar a distribuição de preços em cada um deles.

    Args:
        df (pd.DataFrame): O DataFrame carregado pelo Streamlit.

    Returns:
        matplotlib.figure.Figure: A figura do gráfico boxplot.
    """

    # 2. Tratamento de dados: remover linhas sem informação de preço ou bairro
    # Usamos .copy() para evitar o SettingWithCopyWarning
    df_clean = df.dropna(subset=['price', 'neighborhood']).copy()

    # 3. Filtrar outliers de preço para uma melhor visualização do boxplot
    # Usaremos o método de Z-score para remover valores muito extremos
    df_clean = df_clean[np.abs(df_clean.price - df_clean.price.mean()) <= (3 * df_clean.price.std())]

    # 4. Identificar os 10 bairros com mais anúncios
    top_10_bairros = df_clean['neighborhood'].value_counts().nlargest(10).index

    # 5. Filtrar o DataFrame para conter apenas os dados desses 10 bairros
    df_top_10 = df_clean[df_clean['neighborhood'].isin(top_10_bairros)]

    # 6. Calcular a mediana de preço para cada bairro e ordenar
    ordem_bairros = df_top_10.groupby('neighborhood')['price'].median().sort_values(ascending=False).index

    # 7. Gerar o gráfico
    plt.style.use('seaborn-v0_8-whitegrid')
    # Criamos fig e ax
    fig, ax = plt.subplots(figsize=(14, 8))

    sns.boxplot(
        x='neighborhood',
        y='price',
        data=df_top_10,
        order=ordem_bairros,  # Ordena as caixas pela mediana do preço
        palette='plasma',
        ax=ax  # Informamos ao seaborn para usar o 'ax' que criamos
    )

    ax.set_title('Distribuição de Preços de Apartamentos por Bairro (Top 10)', fontsize=18)
    ax.set_xlabel('Bairro', fontsize=12)
    ax.set_ylabel('Preço (R$)', fontsize=12)

    # Usamos 'ax' para as configurações
    ax.tick_params(axis='x', rotation=45)

    # Formatar o eixo Y para exibir os preços de forma mais legível
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, p: format(int(x), ','))
    )

    fig.tight_layout()

    # 8. Retornar a figura para o Streamlit
    return fig

# Não é mais necessário o "if __name__ == '__main__':"
# pois este script agora é um módulo a ser importado.