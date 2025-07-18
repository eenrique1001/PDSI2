from pydantic import BaseModel

class Mensagem(BaseModel):
    titulo: str
    conteudo: str
    publicada: bool = True

class LinksUFU(BaseModel):
    menuNAV: str
    link: str
    