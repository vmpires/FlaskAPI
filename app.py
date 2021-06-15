from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

f = open('config.json', 'r')
password = json.load(f)

dbroute = "mysql://root:" + password["pass"] + "@localhost/youtube"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = dbroute

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}

# Selecionar Usuários
@app.route('/usuarios', methods=['GET'])
def seleciona_usuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios]
    return response_generator(200, "usuarios", usuarios_json, "Sucesso!")

# Selecionar Usuário específico
@app.route('/usuario/<id>', methods=['GET'])
def seleciona_usuario(id):
    usuario = Usuario.query.filter_by(id=id).first()
    usuario_json = usuario.to_json()
    return response_generator(200, "usuario", usuario_json, "Sucesso!")

# Cadastrar Usuário
@app.route('/usuario', methods=["POST"])
def criar_usuario():
    body = request.get_json()
    # Validar se vieram os parâmetros ou utilizar try/catch para gerar erro
    try:
        usuario = Usuario(nome = body["nome"], email = body["email"])
        db.session.add(usuario)
        db.session.commit()
        return response_generator(201, "usuario", usuario.to_json(), "Usuário criado com sucesso!")
    except Exception as e:
        print('Erro: ', e)
        return response_generator(400, "usuario", {}, "Erro ao cadastrar!")


# Alterar Usuário
@app.route('/usuario/<id>', methods=["PUT"])
def alterar_usuario(id):
    usuario = Usuario.query.filter_by(id=id).first()
    body = request.get_json()
    
    try:
        if ('nome' in body):
            usuario.nome = body['nome']
        if ('email' in body):
            usuario.email = body['email']
        db.session.add(usuario)
        db.session.commit()
        return response_generator(200, "usuario", usuario.to_json(), "Usuário atualizado com sucesso!")
    except Exception as e:
        print('Erro: ', e)
        return response_generator(400, "usuario", {}, "Erro ao atualizar!")

# Excluir Usuário
@app.route('/usuario/<id>', methods=["DELETE"])
def excluir_usuario(id):
    usuario = Usuario.query.filter_by(id=id).first()
    try:
        db.session.delete(usuario)
        db.session.commit()
        return response_generator(200, "usuario", usuario.to_json(), "Usuário excluído com sucesso!")
    except Exception as e:
        print('Erro: ', e)
        return response_generator(400, "usuario", {}, "Erro ao excluir!")

 
def response_generator(status, content_name, content, message=False):
    body = {}
    body[content_name] = content

    if (message):
        body["message"] = message
    
    return Response(json.dumps(body), status=status, mimetype = "application/json")

app.run()