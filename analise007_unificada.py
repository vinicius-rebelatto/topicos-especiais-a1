import pandas as pd
import folium
import json
import matplotlib.pyplot as plt
import io
import base64

def prepara_dados_preco_m2(caminho_arquivo_csv):
    """Prepara o DataFrame calculando o preço mediano por m² para cada bairro."""
    df = pd.read_csv(caminho_arquivo_csv)
    df.dropna(subset=['price', 'usableAreas', 'neighborhood'], inplace=True)
    df = df[df['usableAreas'] > 0]
    df['preco_m2'] = df['price'] / df['usableAreas']

    limite_superior = df['preco_m2'].quantile(0.99)
    df_filtrado = df[df['preco_m2'] < limite_superior]

    preco_m2_mediano = df_filtrado.groupby('neighborhood')['preco_m2'].median()
    return preco_m2_mediano.reset_index()

def criar_grafico_popup(bairro_clicado, preco_m2_bairro, df_todos_precos):
    """Cria um gráfico de barras em imagem para ser usado no popup."""
    df_ordenado = df_todos_precos.sort_values(by='preco_m2', ascending=False).reset_index()

    cores = ['#d3d3d3'] * len(df_ordenado)
    # Adicionado um 'try-except' para o caso de um bairro do mapa não estar nos dados de preço
    try:
        bairro_index = df_ordenado[df_ordenado['neighborhood'] == bairro_clicado].index[0]
        cores[bairro_index] = '#ff4500'
    except IndexError:
        pass # Se não encontrar, apenas deixa todas as barras cinzas

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(df_ordenado['neighborhood'], df_ordenado['preco_m2'], color=cores)
    ax.invert_yaxis()
    ax.set_title(f'Preço/m² em {bairro_clicado}: R$ {preco_m2_bairro:,.2f}')
    ax.set_xlabel('Preço Mediano por m² (R$)')

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)

    html = f'<img src="data:image/png;base64,{b64}">'
    iframe = folium.IFrame(html, width=650, height=450)
    return folium.Popup(iframe, max_width=650)

def gerar_mapa_unificado(caminho_csv, caminho_geojson):
    """Gera o mapa coroplético interativo com popups de gráficos."""
    df_precos = prepara_dados_preco_m2(caminho_csv)

    mapa = folium.Map(location=[-25.45, -49.27], zoom_start=11)

    # --- ALTERAÇÃO PRINCIPAL AQUI ---
    # 1. Carregar os dados do GeoJSON PRIMEIRO, especificando a codificação correta
    with open(caminho_geojson, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # 2. Passar os DADOS JÁ CARREGADOS (e não mais o caminho do arquivo) para o Choropleth
    folium.Choropleth(
        geo_data=geojson_data, # Alterado de caminho_geojson para geojson_data
        name='choropleth',
        data=df_precos,
        columns=['neighborhood', 'preco_m2'],
        key_on='feature.properties.NOME',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Preço Mediano por m² (R$)'
    ).add_to(mapa)

    # O resto do código já usava geojson_data, então não precisa mudar
    for feature in geojson_data['features']:
        nome_bairro = feature['properties']['NOME']
        dados_bairro = df_precos[df_precos['neighborhood'] == nome_bairro]

        if not dados_bairro.empty:
            preco_m2 = dados_bairro.iloc[0]['preco_m2']
            popup_grafico = criar_grafico_popup(nome_bairro, preco_m2, df_precos)

            folium.GeoJson(
                feature,
                style_function=lambda x: {'fillOpacity': 0, 'color': 'transparent', 'weight': 0.5},
                tooltip=f"<b>{nome_bairro}</b><br>R$ {preco_m2:,.2f}/m²",
                popup=popup_grafico
            ).add_to(mapa)

    folium.LayerControl().add_to(mapa)

    nome_arquivo_saida = '07mapa_unificado_curitiba.html'
    mapa.save(nome_arquivo_saida)
    print(f"Mapa unificado '{nome_arquivo_saida}' salvo com sucesso!")

if __name__ == '__main__':
    arquivo_dataset = 'curitiba_apartment_real_estate_data.csv'
    arquivo_geojson = 'curitiba_bairros.geojson'
    gerar_mapa_unificado(arquivo_dataset, arquivo_geojson)