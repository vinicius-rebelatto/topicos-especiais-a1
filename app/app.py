# app/app.py
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

# Importar as análises
from analyses.analysis_001 import run_analysis_001
from analyses.analysis_heatmap import run_heatmap
from analyses.analysis_002 import run_analysis_002
from analyses.analysis_003 import run_analysis_003
from analyses.analysis_004 import run_analysis_004
from analyses.analysis_005 import run_analysis_005
from analyses.analysis_006 import run_analysis_006
from analyses.analysis_007 import run_analysis_007
from analyses.analysis_008 import run_analysis_008

# Configurar a página para usar o layout "wide"
st.set_page_config(layout="wide")
st.title("📊 Análise de Mercado Imobiliário")

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.header("Configurações")
uploaded_file = st.sidebar.file_uploader("Envie seu dataset (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.sidebar.success("Dataset carregado!")

    # --- MENU ATUALIZADO ---
    analysis_options = [
        "Visão Geral dos Dados",
        "Matriz de Correlação",
        "Análise 1: Correlação com Preço",
        "Análise 2: Preço por Bairro",
        "Análise 3: Preço vs. Área Útil",
        "Análise 4: Preço por m² (Top 10)",
        "Análise 5: Preço por Vagas de Garagem",
        "Análise 6: Preço por Número de Quartos",
        "Análise 7: Mapa de Preços por Bairro",
        "Análise 8: Nuvem de Palavras (Luxo)"
    ]

    choice = st.sidebar.radio("Escolha uma análise:", analysis_options)

    # --- PÁGINA PRINCIPAL ---

    if choice == "Visão Geral dos Dados":
        # ... (código da Visão Geral - sem alteração) ...
        st.header("Visão Geral dos Dados")

        st.write("### Amostra do Dataset (5 primeiras linhas)")
        st.dataframe(df.head())

        st.markdown("---")

        st.write("### Dicionário de Dados (Colunas)")
        st.write("Abaixo está uma descrição de cada coluna presente no dataset:")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            * **price**: Preço de venda do imóvel (em R$).
            * **usableAreas**: Área útil (em m²) interna do apartamento.
            * **totalAreas**: Área total (em m²), podendo incluir áreas comuns.
            * **suites**: Número de quartos com banheiro privativo.
            * **bathrooms**: Número total de banheiros no imóvel.
            * **bedrooms**: Número total de quartos (dormitórios).
            * **parkingSpaces**: Número de vagas de garagem.
            * **amenities**: Lista de comodidades do condomínio (ex: 'POOL', 'GYM').
            * **description**: Texto da descrição completa do anúncio.
            """)

        with col2:
            st.markdown("""
            * **title**: Título do anúncio.
            * **zipCode**: CEP (Código de Endereçamento Postal).
            * **lon**: Longitude (coordenada geográfica).
            * **lat**: Latitude (coordenada geográfica).
            * **street**: Nome da rua do imóvel.
            * **neighborhood**: Nome do bairro onde o imóvel está localizado.
            * **poisList**: Lista de Pontos de Interesse (POIs) próximos.
            * **yearlyIptu**: Valor do IPTU (Imposto) anual.
            * **monthlyCondoFee**: Valor da taxa mensal de condomínio.
            """)

    elif choice == "Matriz de Correlação":
        # ... (código do Heatmap - sem alteração) ...
        st.header("Matriz de Correlação (Heatmap)")
        st.write(
            "O gráfico abaixo (heatmap) mostra a correlação entre *todas* as variáveis numéricas do dataset. Ele é útil para ter uma visão geral de quais atributos se movem juntos.")
        st.write(
            "Valores próximos de **1** (azul escuro) indicam forte correlação positiva. Valores próximos de **-1** (vermelho escuro) indicam forte correlação negativa.")

        try:
            fig_heatmap = run_heatmap(df)
            st.pyplot(fig_heatmap)

        except Exception as e:
            st.error(f"Erro ao gerar o heatmap: {e}")
            st.warning("Verifique se o seu CSV possui colunas numéricas.")

    elif choice == "Análise 1: Correlação com Preço":
        # ... (código da Análise 1 - sem alteração) ...
        st.header("Análise 1: Correlação dos Atributos com o Preço")

        st.write(
            "Este gráfico mostra a correlação de Pearson (um 'zoom' na linha 'price' do heatmap) entre os atributos numéricos e o preço do imóvel.")
        try:
            fig_barras = run_analysis_001(df)
            st.pyplot(fig_barras)

        except Exception as e:
            st.error(f"Erro ao gerar a Análise 1: {e}")
            st.warning(
                "Verifique se o seu CSV contém as colunas numéricas esperadas (price, usableAreas, suites, etc.).")

    elif choice == "Análise 2: Preço por Bairro":
        # ... (código da Análise 2 - sem alteração) ...
        st.header("Análise 2: Distribuição de Preços por Bairro")
        st.write(
            "Este gráfico (boxplot) mostra a distribuição dos preços dos imóveis nos **10 bairros com o maior volume de anúncios**. Ele é útil para identificar outliers (pontos) e a faixa de preço (caixa) de cada bairro.")

        try:
            fig_boxplot = run_analysis_002(df)
            st.pyplot(fig_boxplot)

        except Exception as e:
            st.error(f"Erro ao gerar a Análise 2: {e}")
            st.warning("Verifique se o seu CSV contém as colunas 'price' e 'neighborhood'.")

    elif choice == "Análise 3: Preço vs. Área Útil":
        # ... (código da Análise 3 - sem alteração) ...
        st.header("Análise 3: Relação entre Preço e Área Útil")
        st.write(
            "Este gráfico de dispersão (regplot) mostra a relação entre a área útil e o preço do imóvel. A linha vermelha indica a tendência geral (quanto maior a área, maior o preço).")
        st.markdown("*(Nota: Para melhor visualização, os 1% mais extremos de preço e área são filtrados do gráfico)*")

        try:
            fig_regplot = run_analysis_003(df)
            st.pyplot(fig_regplot)

        except Exception as e:
            st.error(f"Erro ao gerar a Análise 3: {e}")
            st.warning("Verifique se o seu CSV contém as colunas 'price' e 'usableAreas'.")

    elif choice == "Análise 4: Preço por m² (Top 10)":
        # ... (código da Análise 4 - sem alteração) ...
        st.header("Análise 4: Preço por Metro Quadrado (Top 10 Bairros)")
        st.write(
            "Esta análise calcula o preço por m² (price / usableAreas) para cada imóvel. Em seguida, agrupa por bairro e calcula a **mediana** do preço/m².")
        st.write("O gráfico exibe os **10 bairros com a mediana de preço/m² mais cara**.")

        try:
            fig_bar_m2 = run_analysis_004(df)
            st.pyplot(fig_bar_m2)

        except Exception as e:
            st.error(f"Erro ao gerar a Análise 4: {e}")
            st.warning("Verifique se o seu CSV contém as colunas 'price', 'usableAreas' e 'neighborhood'.")

    # --- NOVO BLOCO PARA ANÁLISE 5 ---
    elif choice == "Análise 5: Preço por Vagas de Garagem":
        st.header("Análise 5: Preço Médio por Vagas de Garagem")
        st.write(
            "Esta análise mostra como o preço médio dos apartamentos reage à quantidade de vagas de garagem disponíveis (de 0 a 5).")
        st.write(
            "Note como o valor salta significativamente a partir da segunda vaga, sendo um forte indicador de um imóvel de alto padrão.")

        try:
            fig_parking = run_analysis_005(df)
            st.pyplot(fig_parking)
        except Exception as e:
            st.error(f"Erro ao gerar a Análise 5: {e}")
            st.warning("Verifique se o seu CSV contém as colunas 'price' e 'parkingSpaces'.")

    elif choice == "Análise 6: Preço por Número de Quartos":
        st.header("Análise 6: Preço Médio por Número de Quartos")
        st.write(
            "Esta análise, similar à anterior, mostra como o preço médio dos apartamentos reage à quantidade de quartos (de 1 a 6).")
        st.write("Há uma progressão de valor muito clara a cada quarto adicionado.")

        try:
            fig_bedrooms = run_analysis_006(df)
            st.pyplot(fig_bedrooms)
        except Exception as e:
            st.error(f"Erro ao gerar a Análise 6: {e}")
            st.warning("Verifique se o seu CSV contém as colunas 'price' e 'bedrooms'.")


    elif choice == "Análise 7: Mapa de Preços por Bairro":
        st.header("Análise 7: Mapa de Preços por Bairro (Preço/m²)")
        st.write(
            "Este mapa interativo (coroplético) mostra a mediana do preço por metro quadrado em todos os bairros de Curitiba.")
        st.write(
            "Passe o mouse sobre um bairro para ver o nome e clique para ver o valor exato. Use o zoom para explorar.")

        # Conforme sua instrução, o geojson está na raiz, junto com o app.py
        geojson_path = 'curitiba_bairros.geojson'

        try:
            mapa_calor = run_analysis_007(df, geojson_path)

            # Usar st_folium para renderizar o mapa interativo
            st_folium(mapa_calor, height=600, use_container_width=True)

        except FileNotFoundError:
            st.error(f"Erro: Arquivo 'curitiba_bairros.geojson' não encontrado.")
            st.info(
                "Por favor, certifique-se de que o arquivo 'curitiba_bairros.geojson' está na mesma pasta que o 'app.py'.")
        except Exception as e:
            st.error(f"Erro ao gerar a Análise 7: {e}")
            st.warning("Verifique se o seu CSV contém 'price', 'usableAreas' e 'neighborhood'.")


    elif choice == "Análise 8: Nuvem de Palavras (Luxo)":
        st.header("Análise 8: Nuvem de Palavras (Imóveis de Luxo)")
        st.write(
            "Esta análise pega as descrições dos **10% de imóveis mais caros** do dataset e gera uma 'nuvem' com as palavras mais frequentes.")
        st.write(
            "Isso nos ajuda a entender quais termos e características são mais usados para descrever apartamentos de alto padrão (ex: 'cobertura', 'mobiliado', 'design').")
        st.warning("Esta análise requer a biblioteca `wordcloud`. Se o app quebrar, rode: `pip install wordcloud`")

        try:
            fig_wordcloud = run_analysis_008(df)
            st.pyplot(fig_wordcloud)
        except ValueError as ve:
            st.error(f"Erro ao gerar a Análise 8: {ve}")
            st.warning("Verifique se o seu CSV contém as colunas 'price' e 'description'.")
        except Exception as e:
            st.error(f"Erro inesperado ao gerar a Análise 8: {e}")

else:
    st.info("Por favor, envie um arquivo CSV pela barra lateral para começar as análises.")