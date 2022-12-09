from fastapi import FastAPI
import pandas as pd



app = FastAPI()

@app.get("/")
async def read():
    return "primera app"

@app.on_event('startup')
async def startup():
        global df
        df=pd.read_csv("Proyecto.csv")

@app.get('/get_max_duration({year},{platform},{tipo})')
async def get_max_duration(año:int, plataforma:str, duration_type:str):
   #max_duration_id = 0
   if duration_type not in ["min","season"]:
        raise ValueError("duration_type should be 'min' or 'season'")
   elif plataforma not in ["Netflix","Amazon","Disney","Hulu"]:
        raise ValueError("plataforma should be a platform name")
   else:
        if plataforma=="Amazon":
            if duration_type=="min":
                max_duration_id=df[(df["release_year"]==año) & (df["type"]=="Movie")].duration.idxmax()
                return df[(df["plataforma"]=="Amazon")].loc[max_duration_id, 'title']
            if duration_type=="season":
                max_duration_id=df[(df["release_year"]==año) & (df["type"]=="TV Show")].duration.idxmax()
                return df[(df["plataforma"]=="Amazon")].loc[max_duration_id, 'title']
        if plataforma=="Netflix":
            if duration_type=="min":
                max_duration_id=df[(df["release_year"]==año) & (df["type"]=="Movie")].duration.idxmax()
                return df[(df["plataforma"]=="Netflix")].loc[max_duration_id, 'title']
            if duration_type=="season":
                max_duration_id=df[(df["release_year"]==año) & (df["type"]=="TV Show")].duration.idxmax()
                return df[(df["plataforma"]=="Netflix")].loc[max_duration_id, 'title']
        if plataforma=="Hulu":
            if duration_type=="min":
                max_duration_id=df[(df["release_year"]==año) & (df["type"]=="Movie")].duration.idxmax()
                return df[(df["plataforma"]=="Hulu")].loc[max_duration_id, 'title']
            if duration_type=="season":
                max_duration_id=df[(df["release_year"]==año) & (df["type"]=="TV Show")].duration.idxmax()
                return df[(df["plataforma"]=="Hulu")].loc[max_duration_id, 'title']
        if plataforma=="Disney":
            if duration_type=="min":
                max_duration_id=df[(df["release_year"]==año) & (df["type"]=="Movie")].duration.idxmax()
                return df[(df["plataforma"]=="Disney")].loc[max_duration_id, 'title']
            if duration_type=="season":
                max_duration_id=df[(df["release_year"]==año) & (df["type"]=="TV Show")].duration.idxmax()
                return df[(df["plataforma"]=="Disney")].loc[max_duration_id, 'title']


@app.get("/get_count_plataform/{plataforma}")
async def get_count_plataform(plataforma:str):
    if plataforma not in ["Netflix","Amazon","Disney","Hulu"]:
            raise ValueError("plataforma should be a platform name")
    else:
        if plataforma not in ["Netflix","Amazon","Disney","Hulu"]:
                raise ValueError("df. should be a platform name")
        else:
            if plataforma=="Amazon":
                movies=df[(df["type"]=="Movie")&(df["plataforma"]=="Amazon")]["title"].count()
                series=df[(df["type"]=="TV Show")&(df["plataforma"]=="Amazon")]["title"].count()
                dict={"Numeros de serie":series,"Numero de peliculas":movies}
            if plataforma=="Hulu":
                movies=df[(df["type"]=="Movie")&(df["plataforma"]=="Hulu")]["title"].count()
                series=df[(df["type"]=="TV Show")&(df["plataforma"]=="Hulu")]["title"].count()
                dict={"Numeros de serie":series,"Numero de peliculas":movies}
            if plataforma=="Netflix":
                movies=df[(df["type"]=="Movie")&(df["plataforma"]=="Netflix")]["title"].count()
                series=df[(df["type"]=="TV Show")&(df["plataforma"]=="Netflix")]["title"].count()
                dict={"Numeros de serie":series,"Numero de peliculas":movies}
            if plataforma=="Disney":
                movies=df[(df["type"]=="Movie")&(df["plataforma"]=="Disney")]["title"].count()
                series=df[(df["type"]=="TV Show")&(df["plataforma"]=="Disney")]["title"].count()
                dict={"Numeros de serie":series,"Numero de peliculas":movies}
            return  str(dict)


@app.get('/get_listedin/{genero}')
async def get_listedin(genero:str):
    amazon_count=0
    hulu_count=0
    disney_count=0
    netflix_count=0
    for i in df[(df["plataforma"]=="Amazon")]["listed_in"]:
        if genero in i.split(","):
            amazon_count+=1
    for i in df[(df["plataforma"]=="Netflix")]["listed_in"]:
        if genero in i.split(","):
            netflix_count+=1
    for i in df[(df["plataforma"]=="Hulu")]["listed_in"]:
        if genero in i.split(","):
            hulu_count+=1
    for i in df[(df["plataforma"]=="Disney")]["listed_in"]:
        if genero in i.split(","):
            disney_count+=1
    dict_count={"Amazon":amazon_count,"Netflix":netflix_count,"Hulu":hulu_count,"Disney":disney_count}
    max_value=max(dict_count.values())
    max_platform=key = [key for key, val in dict_count.items() if val == max_value][0]
    return max_platform , max_value

@app.get('/get_actor{plataforma},{año}')
async def get_actor(plataforma:str,año:int):

    df_plataforma=(df[(df.plataforma==plataforma)&(df.release_year==año)&(df.cast!='Desconocido')])
    df_plataforma['cast']=df_plataforma['cast'].replace(' ,',',') 
    df_plataforma['cast']=df_plataforma['cast'].replace(', ',',') 

    lista_actores_unicos=[]

    for lista in df_plataforma['cast']:
        lista=str(lista).split(',')
    for actor in lista:
            actor=actor.strip()
            lista_actores_unicos.append(actor)
    lista_actores_unicos=list(set(lista_actores_unicos))

    lista_actores=[]
    lista_repetidos=[]
    dicc={}

    for lista in df_plataforma['cast']:
            lista=str(lista).split(',')
            for actor in lista:
                actor=actor.strip()
                lista_actores.append(actor)
    lista_actores_unicos=list(set(lista_actores))

    for i,e in enumerate(lista_actores):
            contador=lista_actores.count(e)
            dicc[e]=contador
        
    a=max(dicc, key=dicc.get)

    m=dicc.get(a)
    rta= str(a) + ' ' +str(m)
    return  str(rta)