import pandas as pd
import folium
from folium.plugins import HeatMap


def gerar_mapa_interativo(caminho_arquivo):
    """
    Carrega o dataset e gera um mapa de calor interativo dos preços
    dos imóveis sobre um mapa real de Curitiba.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV do dataset.
    """
    # 1. Carregar o dataset
    df = pd.read_csv(caminho_arquivo)

    # 2. Tratamento de dados: remover linhas sem lat, lon ou preço
    df.dropna(subset=['price', 'lat', 'lon'], inplace=True)

    # 3. Limitar os dados para uma visualização mais limpa e performática
    # Usaremos apenas imóveis abaixo do quantil 95% para focar na maioria do mercado
    limite_preco = df['price'].quantile(0.95)
    df_filtrado = df[df['price'] <= limite_preco]

    # 4. Criar o mapa base centrado em Curitiba
    # As coordenadas (-25.4284, -49.2733) são o centro aproximado de Curitiba
    mapa_curitiba = folium.Map(location=[-25.4284, -49.2733], zoom_start=12)

    # 5. Preparar os dados para o mapa de calor
    # A HeatMap espera uma lista de listas no formato: [[latitude, longitude, peso]]
    # O 'peso' aqui será o preço do imóvel, que determinará a 'intensidade' do calor
    dados_heatmap = df_filtrado[['lat', 'lon', 'price']].values.tolist()

    # 6. Adicionar a camada de mapa de calor ao mapa base
    HeatMap(dados_heatmap,
            radius=15,
            blur=20,
            gradient={0.2: 'blue', 0.4: 'green', 0.6: 'yellow', 1: 'red'}
            ).add_to(mapa_curitiba)

    # 7. Salvar o mapa em um arquivo HTML
    nome_arquivo_saida = '07mapa_de_calor_curitiba.html'
    mapa_curitiba.save(nome_arquivo_saida)
    print(f"Mapa interativo '{nome_arquivo_saida}' salvo com sucesso!")
    print("Abra este arquivo em um navegador para ver o resultado.")


if __name__ == '__main__':
    # Você precisa ter a biblioteca folium instalada: pip install folium
    arquivo_dataset = 'curitiba_apartment_real_estate_data.csv'
    gerar_mapa_interativo(arquivo_dataset)