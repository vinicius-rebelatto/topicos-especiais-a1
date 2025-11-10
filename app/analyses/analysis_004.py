import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


def run_analysis_004(df):
    """
    Recebe um DataFrame, calcula o preço por m², filtra outliers,
    e gera um gráfico de barras com o preço/m² mediano para os
    10 bairros mais caros.
    Retorna uma figura matplotlib.
    """

    # 2. Selecionar colunas e tratar nulos
    colunas_analise = ['price', 'usableAreas', 'neighborhood']

    colunas_faltando = [col for col in colunas_analise if col not in df.columns]
    if colunas_faltando:
        raise ValueError(f"Colunas necessárias não encontradas: {', '.join(colunas_faltando)}")

    df_clean = df[colunas_analise].dropna().copy()

    # 3. Filtrar outliers para um cálculo de m² mais justo
    # (Ex: áreas muito pequenas ou preços muito baixos podem distorcer)
    df_clean = df_clean[
        (df_clean['usableAreas'] > 10) &  # Remover áreas 'zero' ou muito pequenas
        (df_clean['price'] > 1000)  # Remover preços 'zero' ou simbólicos
        ]

    # 4. Engenharia de Atributo: Calcular o preço por m²
    df_clean['price_per_m2'] = df_clean['price'] / df_clean['usableAreas']

    # 5. Calcular a mediana do preço/m² por bairro
    # A mediana é usada para ser menos sensível a mansões/outliers
    bairro_m2_median = df_clean.groupby('neighborhood')['price_per_m2'].median()

    # 6. Identificar os 10 bairros com maior mediana de preço/m²
    top_10_caros = bairro_m2_median.sort_values(ascending=False).head(10)

    if top_10_caros.empty:
        raise ValueError("Não foi possível calcular o m² por bairro (sem dados suficientes).")

    # 7. Gerar o gráfico
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(
        x=top_10_caros.index,
        y=top_10_caros.values,
        palette='rocket',
        hue=top_10_caros.index,  # Adicionado para o novo padrão
        legend=False,
        ax=ax
    )

    # Adicionar os valores nas barras
    for p in ax.patches:
        ax.annotate(f'R$ {p.get_height():,.2f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points')

    ax.set_title('Top 10 Bairros por Preço Mediano do m²', fontsize=16)
    ax.set_xlabel('Bairro', fontsize=12)
    ax.set_ylabel('Preço Mediano por m² (R$)', fontsize=12)

    # Formatar eixo Y (Preço/m²)
    formatter = FuncFormatter(lambda y, p: f'R$ {y:,.0f}')
    ax.get_yaxis().set_major_formatter(formatter)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    fig.tight_layout()

    return fig