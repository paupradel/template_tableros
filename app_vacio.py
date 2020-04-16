# Este script contiene el esqueleto de un tablero de dash, incluyendo únicamente el encabezado con título y logo de conacyt.

# Importar bibliotecas
# Agregar las bibliotecas necesarias dependiendo de las necesidades del proyecto

import dash
import dash_html_components as html  # Componentes html para usar en dash

# Inicializar la app de dash
app = dash.Dash(__name__)

# -----------------------------------------  HTML ----------------------------------------------#
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

    <!-- Agregar un favicon (en el folder de assets) a la app (por default aquí está el de conacyt) -->
    {%favicon%}
    {%css%}
</head>
<body>
{%app_entry%}
{%config%}
{%scripts%}
{%renderer%}
</body>
</html>'''

# Construir layout
app.layout = html.Div([html.Div([html.H1('Título del tablero', className='a', id='a'),
                                 html.Img(src=app.get_asset_url('conacyt.png'), alt='logo de conacyt',
                                          className='logo')], className='header', id='header'),
                       html.Div([html.Div([html.Div('four', className='four columns'),
                                           html.Div('eight', className='eight columns')], className='row'),
                                 html.Div([html.Div('five', className='five columns'),
                                           html.Div('seven', className='seven columns')], className='row'),
                                 html.Div([html.Div('six', className='six columns'),
                                           html.Div('seven', className='six columns')], className='row')],
                                className='grid', id='grid')], className='container', id='container')

if __name__ == '__main__':
    app.run_server(debug=True)
