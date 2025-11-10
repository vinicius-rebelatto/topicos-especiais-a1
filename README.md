# 📊 Análise Interativa de Imóveis em Curitiba

Este é um painel (dashboard) interativo desenvolvido em Python e Streamlit, focado na análise exploratória de um dataset de apartamentos em Curitiba.

A aplicação permite ao usuário carregar um dataset (`.csv`) e visualizar de forma interativa os principais fatores que influenciam o preço dos imóveis, desde a correlação de atributos básicos até a localização geográfica e as palavras-chave usadas em anúncios de luxo.



## 📄 O Dataset

A análise foi projetada para funcionar com um dataset de anúncios de imóveis (como o `curitiba_apartment_real_estate_data.csv`). As colunas-chave utilizadas nas análises são:

* **`price`**: O valor de venda do imóvel.
* **`usableAreas`**: A área útil em m².
* **`neighborhood`**: O bairro onde o imóvel se localiza.
* **`bedrooms`**: Número de quartos.
* **`parkingSpaces`**: Número de vagas de garagem.
* **`lat` / `lon`**: Coordenadas geográficas.
* **`description`**: O texto do anúncio.
* **`amenities`**: Lista de comodidades (ex: 'POOL', 'GYM').

## 📈 Análises Disponíveis

O painel é dividido nas seguintes seções:

* **Visão Geral dos Dados**: Exibe as primeiras linhas do dataset e um dicionário de dados explicando cada coluna.
* **Matriz de Correlação**: Um mapa de calor (heatmap) que mostra a correlação entre *todas* as variáveis numéricas do dataset.
* **Análise 1: Correlação com Preço**: Um gráfico de barras focado: quais atributos mais afetam o `price`?
* **Análise 2: Preço por Bairro**: Um boxplot que compara a faixa de preços (mediana, quartis e outliers) nos 10 bairros com mais anúncios.
* **Análise 3: Preço vs. Área Útil**: Gráfico de dispersão que mostra a clara tendência de que apartamentos maiores custam mais.
* **Análise 4: Preço por m² (Top 10)**: O verdadeiro "custo-benefício". Mostra o ranking dos 10 bairros com o metro quadrado mediano mais caro.
* **Análise 5: Preço por Vagas de Garagem**: Gráfico de barras que quantifica o quanto o preço médio sobe para cada vaga de garagem adicional.
* **Análise 6: Preço por Número de Quartos**: Similar ao anterior, mostra o preço médio de apartamentos com 1, 2, 3+ quartos.
* **Análise 7: Mapa de Preços por Bairro**: O mapa interativo (coroplético) que colore os bairros de Curitiba com base no seu preço/m² mediano. A "geografia do dinheiro".
* **Análise 8: Nuvem de Palavras (Luxo)**: Uma nuvem de palavras com os termos mais frequentes nas descrições dos 10% de imóveis mais caros.

## 🚀 Como Executar o Projeto

Siga os passos abaixo para rodar a aplicação na sua máquina local.

### 1. Dependências

Você precisa ter o Python 3.x instalado. As bibliotecas necessárias podem ser instaladas com:

```bash
pip install streamlit pandas matplotlib seaborn folium streamlit-folium wordcloud