# Template de tablero

#### -- Estatus del proyecto: [Activo]

## 1. Acerca de este proyecto
Usando el código de este repositorio es posible crear tableros usando 
el framework de python [Dash](https://dash.plot.ly/).

El objetivo es reutilizar el código, producir y personalizar tableros 
de análisis a demanda y de una manera rápida.

### 1.1 Métodos usados
* Visualización de datos
* Desarrollo web

### 1.2 Tecnologías usadas
* Python
* Pandas
* Plotly
* Dash
* HTML
* CSS

## 2. Descripción del proyecto

Usando el framework de python [Dash](https://dash.plotly.com/) se creó un template de tableros en donde se pueden 
presentar análisis de datos con gráficas construidas usando la biblioteca de [plotly](https://plotly.com/python/).

Uno de los principales objetivos de este proyecto fué constrtuir un tablero responsivo y que se pudiera consultar 
en dispositivos móviles como los teléfonos inteligentes. Para ello se usaron estilos de ```CSS``` basados en [esta guía 
de estilo](https://codepen.io/chriddyp/pen/bWLwgP) creada por [Chris Parmer](https://github.com/chriddyp).

La construcción de las gráficas se puede consultar en un jupyter notebook en la carpeta ```/chart_demos/demos_graficas.ipynb```.
Se construyeron de manera que su inclusión al template fuera sencilla.

Una explicación más detallada se puede encontrar en la Wiki de este proyecto.

## 2.1 ¿Cómo empezar?

1. Clona este repositorio (aquí un [tutorial](https://help.github.com/articles/cloning-a-repository/)).

2. Los datos que usan los ejemplos de las gráficas en plotly están guardados en este [folder](https://gitlab.ccd.conacyt.mx/analisis/template_tableros/tree/develop/chart_demos/data) 
del repositorio. Son datos libres.
    
3. Los notebooks de jupyter que contienen los ejemplos de gráficas realizadas en 
 plotly y adaptadas a dash se encuentran en este [folder](https://gitlab.ccd.conacyt.mx/analisis/template_tableros/tree/develop/chart_demos).

4. Para poder utilizar el código se recomienda [crear un ambiente virtual](https://vitux.com/install-python3-on-ubuntu-and-set-up-a-virtual-programming-environment/) e 
instalar las bibliotecas necesarias vía el archivo [```requirements.txt```](https://gitlab.ccd.conacyt.mx/analisis/template_tableros) de este repositorio. 
Lo anterior se puede hacer en la terminal (linux) mediante el siguiente comando.

    ```$ pip install -r requirements.txt```

## Contacto

- Paulina Pradel, @pradel (gitlab), pradel.paulina@ciencias.unam.mx