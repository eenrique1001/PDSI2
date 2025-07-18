#para rodar: uvicorn main:app

from fastapi import FastAPI, status, Depends
import classes
import model
from database import engine, get_db
from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup
from typing import List
from fastapi.middleware.cors import CORSMiddleware

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())

    #mensagem_criada = model.Model_Mensagem( titulo=nova_mensagem.titulo,
    #conteudo=nova_mensagem.conteudo, publicada=nova_mensagem.publicada)

    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}


@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 2


@app.get("/armazenarLinks", status_code=status.HTTP_200_OK)
def enviarLinks(db: Session = Depends(get_db)):

    try:
        resposta = requests.get("https://www.ufu.br", timeout=10)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return {"erro": "Site indisponível no momento. Tente novamente mais tarde."}
    
    if(resposta.status_code == 200): 
        soup = BeautifulSoup(resposta.content, 'html.parser') 
        print(soup.prettify())
        barra_esquerda = soup.find('ul', class_='sidebar-nav nav-level-0')
        linhas_barra_esquerda = barra_esquerda.find_all('li', class_='nav-item')
        iniciar_captura = False
        linhas_desejadas_barra_esquerda = []
        links_barra_esquerda = []
        combined = []
        for li in linhas_barra_esquerda:
            if 'Graduação' in li.text.strip():
                iniciar_captura = True
            if iniciar_captura:
                combined.append((li.text.strip(), "https://ufu.br"+li.a.get('href')))
                #linhas_desejadas_barra_esquerda.append(li.text.strip())
                #links_barra_esquerda.append("https://ufu.br"+li.a.get('href'))

        print(linhas_desejadas_barra_esquerda)
        print(links_barra_esquerda)
    
        #rows = [model.Model_Links(menuNAV=t[0], link=t[1]) for t in combined]
        #db.add_all()

        for a, b in combined:
            link = model.Model_Links(menuNAV=a, link=b)
            db.add(link)
            db.refresh(link)
        db.commit()
    return {"msg": "links criados com sucesso"}

@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int=100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens