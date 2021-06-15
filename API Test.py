import requests
import json

def BuscaUsuarios():
    request = requests.get('http://127.0.0.1:5000/usuarios') 
    usuarios = request.json()
    
    for item in range(len(usuarios["usuarios"])):
       print(f"Usuário ID {usuarios['usuarios'][item]['id']}: {usuarios['usuarios'][item]['nome']}")
       print(f"E-mail: {usuarios['usuarios'][item]['email']}")

BuscaUsuarios()