# analyses/analysis_008.py
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re
from collections import Counter


def run_analysis_008(df):
    """
    Gera uma nuvem de palavras com as descrições dos 10% de imóveis mais caros.

    Args:
        df (pd.DataFrame): O DataFrame carregado.

    Returns:
        matplotlib.figure.Figure: A figura da nuvem de palavras.
    """

    # 1. Verificação das colunas
    if "price" not in df.columns or "description" not in df.columns:
        raise ValueError("O arquivo precisa conter as colunas 'price' e 'description'.")

    # 2. Selecionar os 10% imóveis mais caros
    df_clean = df.dropna(subset=["price", "description"]).copy()
    limite_top_10 = df_clean["price"].quantile(0.90)
    df_top10 = df_clean[df_clean["price"] >= limite_top_10]

    # 3. Juntar todas as descrições em um único texto
    texto_completo = " ".join(df_top10["description"].astype(str).tolist())

    # 4. Limpeza básica do texto
    texto_completo = re.sub(r'<[^>]+>', ' ', texto_completo)  # Remove tags HTML (ex: <br>)
    texto_completo = texto_completo.lower()  # Converte para minúsculas

    # 5. Stopwords (português + termos imobiliários)
    stopwords_pt = set(STOPWORDS)
    stopwords_pt.update([
        "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas", "que", "e", "com", "para", "por",
        "um", "uma", "uns", "umas", "ao", "à", "a", "os", "as", "se", "nao", "não", "ou", "mais", "também",
        "apartamento", "apto", "imovel", "imóvel", "condominio", "condomínio", "m2", "m²", "area", "área",
        "quartos", "quarto", "dormitórios", "dormitório", "suite", "suíte", "banheiro", "banheiros",
        "vaga", "vagas", "andar", "sala", "cozinha", "metragem", "valor", "novo", "completamente",
        "m", "x", "r$", "ser", "localizado", "proximo", "próximo", "regiao", "região", "curitiba"
    ])

    # 6. Geração da nuvem
    nuvem = WordCloud(
        width=1200,
        height=700,
        background_color="white",
        stopwords=stopwords_pt,
        colormap="viridis",
        min_font_size=10,
        max_words=100
    ).generate(texto_completo)

    # 7. Geração da Figura
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.imshow(nuvem, interpolation='bilinear')
    ax.axis("off")  # Remove os eixos x e y

    fig.tight_layout(pad=0)

    # 8. Retornar a figura para o Streamlit
    return fig