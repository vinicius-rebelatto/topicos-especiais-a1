import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


def run_analysis_003(df):
    """
    Recebe um DataFrame, trata nulos, filtra outliers e gera um
    gráfico de dispersão (regplot) entre preço e área útil.
    Retorna uma figura matplotlib.
    """

    # 2. Selecionar colunas e tratar nulos
    colunas_analise = ['price', 'usableAreas']

    colunas_faltando = [col for col in colunas_analise if col not in df.columns]
    if colunas_faltando:
        raise ValueError(f"Colunas necessárias não encontradas: {', '.join(colunas_faltando)}")

    df_analise = df[colunas_analise].dropna().copy()

    # 3. Filtrar outliers extremos para melhor visualização
    # Usamos o método do quantil para pegar os 98% centrais dos dados
    q_low_price = df_analise['price'].quantile(0.01)
    q_high_price = df_analise['price'].quantile(0.99)

    q_low_area = df_analise['usableAreas'].quantile(0.01)
    q_high_area = df_analise['usableAreas'].quantile(0.99)

    df_filtrado = df_analise[
        (df_analise['price'] >= q_low_price) &
        (df_analise['price'] <= q_high_price) &
        (df_analise['usableAreas'] >= q_low_area) &
        (df_analise['usableAreas'] <= q_high_area)
        ]

    if df_filtrado.empty:
        raise ValueError("Não há dados suficientes após a remoção de outliers.")

    # 4. Gerar o gráfico (regplot para mostrar a linha de tendência)
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.regplot(
        x='usableAreas',
        y='price',
        data=df_filtrado,
        ax=ax,
        scatter_kws={'alpha': 0.3, 's': 10},  # Pontos semitransparentes
        line_kws={'color': 'red'}  # Linha de tendência vermelha
    )

    # 5. Formatação e títulos
    ax.set_title('Relação entre Preço e Área Útil (Filtrando Outliers)', fontsize=16)
    ax.set_xlabel('Área Útil (m²)', fontsize=12)
    ax.set_ylabel('Preço (R$)', fontsize=12)

    # Formatar eixo Y (Preço)
    formatter_price = FuncFormatter(lambda x, p: f'R$ {x:,.0f}')
    ax.get_yaxis().set_major_formatter(formatter_price)

    # Formatar eixo X (Área)
    formatter_area = FuncFormatter(lambda x, p: f'{x:,.0f} m²')
    ax.get_xaxis().set_major_formatter(formatter_area)

    fig.tight_layout()

    return fig