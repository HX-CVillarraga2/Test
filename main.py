from fastapi import FastAPI
import pandas as pd 

app=FastAPI()

@app.get('/')
async def root():
    return {'message':'Holi'}

datos = pd.read_csv('clean.csv')

@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    """
    Devuelve el nombre del video con la duración más larga para los parámetros de entrada proporcionados.

    year: Año de lanzamiento del video.
    platform: Plataforma en la que está disponible el video.
    duration_type: Tipo de duración del video (minutos o temporadas).
    """
    
    #Filtro los datos segun parametros de entrada
    datos_filtrados = datos.loc[(datos['release_year'] == anio) & (datos['plataforma'] == plataforma) & (datos['duration_type'] == dtype)]

    if datos_filtrados.empty:
        return {"message": "No se encontraron resultados para los parámetros proporcionados."}
    
    #Obtengo el valor mas alto de los datos filtrados en duration_int
    max_index=datos_filtrados['duration_int'].idxmax()

    #Pelicula/serie con mayor duration
    title_max = datos_filtrados.loc[max_index, 'title']

    
    return {'pelicula': title_max}

@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):
    
    datos_filtrados = datos.loc[(datos['release_year'] == anio) & (datos['plataforma'] == plataforma) & (datos['scored'] >= scored)]
    
    #Cantidad de películas
    respuesta=datos_filtrados.shape[0]
    
    return {
        'plataforma': plataforma,
        'cantidad': respuesta,
        'anio': anio,
        'score': scored
    }

"""
La cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año. 
La función debe llamarse prod_per_county(tipo,pais,anio) deberia devolver el tipo de contenido 
(pelicula,serie,documental) por pais y año en un diccionario con las variables llamadas 'pais' (nombre del pais), 'anio' (año), 
'pelicula' (tipo de contenido).
"""
@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):
    
    datos_filtrados = datos.loc[(datos['country'].str.contains(pais)) & (datos['release_year'] == anio) & (datos['type'] == tipo)]


    respuesta=datos_filtrados.shape[0]
    return {'pais': pais, 'anio': anio, 'peliculas': respuesta}


"""
La cantidad total de contenidos/productos (todo lo disponible en streaming, series, documentales, peliculas, etc) 
según el rating de audiencia dado (para que publico fue clasificada la pelicula). La función debe llamarse get_contents(rating) y debe devolver el numero total de contenido con ese rating de audiencias.

# """
# @app.get('/get_recomendation/{title}')
# def get_recomendation(title,):
    
#     return {'recomendacion':respuesta}

    

    
