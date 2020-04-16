# Este script contiene un demo de tablero de dash, incluyendo las siguientes gráficas:
# - Tabla
# - De barras
# - De líneas
# - De pie
# - Mapa coroplético

# Cada uno de estas gráficas y detalles de su construcción e inclusión en este tablero pueden ser encontradas en el
# notebook de jupyter en la carpeta /chart_demos de este proyecto.


# Importar bibliotecas
# Agregar las bibliotecas necesarias dependiendo de las necesidades del proyecto

import os
import dash
import dash_auth
import dash_core_components as dcc  # Componentes principales de dash (dropdowns, sliders, etc.)
import dash_html_components as html  # Componentes html para usar en dash
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

# Especificar las credenciales para acceder al tablero como variables de entorno
VALID_USERNAME_PASSWORD_PAIRS = {os.environ['USER']: os.environ['PASSWORD']}

# Inicializar la app de dash
app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

# ---------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------------  HTML ------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------- #

# Personalización del template de html (head, fuente de texto, favicon, etc.).
app.index_string = '''
<!DOCTYPE html>
<html>  
<head>
    <!-- Se usan google fonts, cambiar a demanda la url de la fuente y modificar en el css -->
    <link href="https://fonts.googleapis.com/css?family=Sen&display=swap" rel="stylesheet">
    
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="author" content="pradel">
    
    <!-- Cambiar el título de la app (el que aparece en la pestaña del navegador) -->
    <title>Título</title>
    
    <!-- Agregar un favicon (en el folder de assets) a la app (por default está el de dash) y colocarlo de la-->
    <!-- siguiente manera: -->
    <!-- {%favicon%}-->
    {%css%}
</head>
<body>
{%app_entry%}
{%config%}
{%scripts%}
{%renderer%}
</body>
</html>'''

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- DATAFRAMES ------------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #

# Dataframe del que se obtienen los datos a graficar y reestructuración de algunos datos
df = pd.read_csv('chart_demos/data/df_housing.csv')

# Dataframe de datos de población que se usa para el mapa coroplético
df_mexico = pd.read_csv('chart_demos/data/mexico_edos.csv')

# ---------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------- GRÁFICAS DE PLOTLY ---------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

# El detalle de la construcción de las siguientes gráficas se puede encontrar en el notebook demos_graficas.ipynb

# -------------------------------------------------TABLA---------------------------------------------------------------#

# Se obtiene en número de ventas que se realizaron cada año contando el número de registros existentes.
NumSales = df.groupby('YrSold').size().tolist()

# Se obtienen los valores únicos para cada año
YrSold = df['YrSold'].unique().tolist()
YrSold.sort()

# ------- --Definir encabezados y colores ------------#
# Encabezado de la tabla
tabla_encabezado = ['Año de venta', 'Número de ventas']

# Datos de la tabla
tabla_valores = [YrSold, NumSales]

# Colores de las celdas
color_header = 'white'
color_fila_impar = '#8080ff'
color_fila_par = '#e6e6ff'

colores_filas = [[color_fila_impar, color_fila_par, color_fila_impar, color_fila_par, color_fila_impar] * 5]

# -------Construir la tabla y el layout de la figura --------#
data_tabla = go.Table(header={'values': tabla_encabezado,
                              'fill': {'color': color_header},
                              'align': 'left',
                              'line': {'color': '#f5f5f5',
                                       'width': 1}},
                      cells={'values': tabla_valores,
                             'align': 'left',
                             'fill': {'color': colores_filas},
                             'line': {'color': '#f5f5f5',
                                      'width': 1}})

layout_tabla = go.Layout(paper_bgcolor='#f5f5f5',
                         plot_bgcolor='#f5f5f5',
                         font={'family': 'Sen'},
                         margin={'autoexpand': True,
                                 'pad': 5},
                         autosize=True)

# ------- Construir la figura que se muestra en dash --------#
figura_tabla = {'data': [data_tabla],
                'layout': layout_tabla}

# ---------------------------------------------GRÁFICA DE BARRAS ------------------------------------------------------#

# Valores categóricos de las condiciones de venta
condicionVenta = df['SaleCondition'].unique().tolist()

# Se ordenan los valores categóricos para que coincidan con la frecuencia de registros obtenidos.
# Este paso es muy importante pues se corre el riesgo de no obtener la asignación de valores correcta.
condicionVenta.sort()

# Cantidad de casas con determinada condición de venta
numCondicionVenta = df.groupby('SaleCondition').size().tolist()

# -------- Asignar datos y construir layout de gráfica de barras --------#
data_barras = go.Bar(x=condicionVenta,
                     y=numCondicionVenta,
                     marker_color='purple')

layout_barras = go.Layout(xaxis={'categoryorder': 'total descending'})

# ------------ Construir la figura que se muestra en dash ---------------#
figura_barras = {'data': [data_barras],
                 'layout': layout_barras}

# --------------------------------------------- GRÁFICA DE PIE-------------------------------------------------------- #

# Se grafica el pie, usando las columnas adecuadas y los valores de layout también se determinan aquí
figura_pie = px.pie(df,
                    values=NumSales,
                    names=YrSold,
                    color_discrete_sequence=px.colors.sequential.RdBu)

# -------------------------------------------- GRÁFICA DE LÍNEAS ----------------------------------------------------- #
# Se filtar el dataframe con las dos columnas que se necesitan
df_lineas = df[['YrSold', 'SalePrice']]

# Se agrupa usando una suma sobre SalePrice por año
df_lineas = df_lineas.groupby('YrSold', as_index=False).sum()

# ----------------- Asignar datos y construir layout de gráfica de líneas --------------------------#
data_lineas = go.Scatter(x=df_lineas['YrSold'],
                         y=df_lineas['SalePrice'],
                         mode='lines+markers',
                         line={'color': 'firebrick',
                               'width': 4})

layout_lineas = go.Layout(title={'text': '<b>Importe generado por año</b>'},
                          xaxis={'nticks': 5})

# ----------------- Construir la figura que se muestra en dash -----------------------------#
figura_lineas = {'data': [data_lineas],
                 'layout': layout_lineas}

# ---------------------------------------------- MAPA COROPLÉTICO ---------------------------------------------------- #
# Se carga el archivo json que contiene la geometría adecuada para graficar
with open('chart_demos/data/mexico_edos.json') as geofile:
    jdata = json.load(geofile)

# Se define el argumento locations como una lista obteniéndose del identificador de las localidades
# en el dataframe.
locations = df_mexico['id'].tolist()

# Asignaciones de colores de la densidad poblacional.
z_densidad = df_mexico['densidad_poblacion'].tolist()

# ----------------- Asignar datos y construir layout del mapa --------------------------#
data_mapa_densidad = go.Choroplethmapbox(geojson=jdata,
                                         locations=locations,
                                         z=z_densidad,
                                         colorscale='algae')

layout_mapa_densidad = go.Layout(mapbox={'center': {'lat': 23.6345005,
                                                    'lon': -102.5527878},
                                         'style': 'carto-positron',
                                         'zoom': 4},
                                 margin={'l': 0,
                                         'r': 0,
                                         't': 5,
                                         'b': 15}, )

# ----------------- Construir la figura que se muestra en dash -----------------------------#
fig_mapa_densidad = go.Figure(data=data_mapa_densidad, layout=layout_mapa_densidad)

# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------LAYOUT DEL TABLERO---------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

# Construir layout de la app e incluir las gráficas como figure
app.layout = html.Div([html.Div([html.H1('Título del tablero', className='a', id='a'),
                                 html.A([html.Img(src=app.get_asset_url('GitHub_Logo.png'), alt='logo github',
                                                  className='logo')],
                                        href='https://github.com/paupradel/template_tableros')], className='header',
                                id='header'),
                       html.Div([html.Div([html.Div([dcc.Graph(figure=figura_tabla)], className='four columns'),
                                           html.Div([dcc.Graph(figure=figura_barras)], className='eight columns')],
                                          className='row'),
                                 html.Div([html.Div([dcc.Graph(figure=figura_pie)], className='five columns'),
                                           html.Div([dcc.Graph(figure=figura_lineas)], className='seven columns')],
                                          className='row'),
                                 html.Div([html.Div(html.Article([html.H2('A Word on the Recent Catnip Doping Scandal'),
                                                                  html.P(
                                                                      "The influence that catnip has on feline behavior "
                                                                      "is well-documented, and its use as an herbal "
                                                                      "supplement in competitive ninja circles remains "
                                                                      "controversial. Once again, the debate to ban the "
                                                                      "substance is brought to the public's attention "
                                                                      "after the high-profile win of Kittytron, a "
                                                                      "long-time proponent and user of the green stuff, "
                                                                      "at the Claw of Fury tournament."),
                                                                  html.P(
                                                                      "As I've stated in the past, I firmly believe a "
                                                                      "true ninja's skills must come from within, with "
                                                                      "no external influences. My own catnip use shall "
                                                                      "continue as purely recreational.")]),
                                                    className='six columns'),
                                           html.Div([dcc.Graph(figure=fig_mapa_densidad)], className='six columns')],
                                          className='row')],
                                className='grid', id='grid')], className='container', id='container')

if __name__ == '__main__':
    app.run_server(debug=True)
