# analyses/analysis_007.py
import pandas as pd
import folium
import json


# --- FUNÇÃO 1 (HELPER) ---
# Colocada no topo do arquivo (nível principal)
def prepara_dados_preco_m2(df):
    """Prepara o DataFrame calculando o preço mediano por m² para cada bairro."""
    df_clean = df.dropna(subset=['price', 'usableAreas', 'neighborhood']).copy()
    df_clean = df_clean[df_clean['usableAreas'] > 0]

    df_clean['preco_m2'] = df_clean['price'] / df_clean['usableAreas']

    limite_superior = df_clean['preco_m2'].quantile(0.99)
    df_filtrado = df_clean[df_clean['preco_m2'] < limite_superior]

    preco_m2_mediano = df_filtrado.groupby('neighborhood')['preco_m2'].median()
    return preco_m2_mediano.reset_index()


# --- FUNÇÃO 2 (PRINCIPAL) ---
# Também no topo do arquivo (nível principal)
def run_analysis_007(df, geojson_path):
    """
    Gera um mapa coroplético interativo do preço por m² nos bairros.
    (Esta é a função que o app.py vai chamar)
    """

    # 1. Preparar os dados de preço
    df_precos = prepara_dados_preco_m2(df)

    # 2. Criar o mapa base
    mapa = folium.Map(location=[-25.45, -49.27], zoom_start=11)

    # 3. Ler o GeoJSON
    try:
        with open(geojson_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo GeoJSON não encontrado em: {geojson_path}")
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo GeoJSON: {e}")

    # 4. Adicionar a camada de cor (Choropleth)
    folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=df_precos,
        columns=['neighborhood', 'preco_m2'],
        key_on='feature.properties.NOME',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Preço Mediano por m² (R$)'
    ).add_to(mapa)

    # 5. Adicionar camada de interatividade (tooltips/popups)
    preco_dict = df_precos.set_index('neighborhood')['preco_m2']

    for feature in geojson_data['features']:
        nome_bairro = feature['properties']['NOME']
        preco_m2 = preco_dict.get(nome_bairro)

        if pd.notna(preco_m2):
            popup_text = f"<b>{nome_bairro}</b><br>R$ {preco_m2:,.2f} / m²"

            folium.GeoJson(
                feature,
                style_function=lambda x: {'fillOpacity': 0, 'color': 'transparent'},
                tooltip=nome_bairro,
                popup=folium.Popup(popup_text, max_width=300),
                highlight_function=lambda x: {'weight': 2, 'color': 'black', 'fillOpacity': 0.1},
            ).add_to(mapa)

    folium.LayerControl().add_to(mapa)

    # 6. Retornar o objeto do mapa
    return mapa