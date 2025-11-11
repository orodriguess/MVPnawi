from flask_restx import Namespace, Resource, fields
from flask import request
from backend.database.config import db
from backend.models.usuarios import Usuario

api = Namespace('usuarios', description='Operações com usuários')

# Modelo para documentação no Swagger
usuario_model = api.model('Usuario', {
    'id': fields.Integer(readonly=True, description='ID do usuário'),
    'nome': fields.String(required=True, description='Nome do usuário'),
    'email': fields.String(required=True, description='E-mail do usuário')
})

# ---------- ROTAS PRINCIPAIS ----------

@api.route('/')
class UsuariosList(Resource):
    @api.marshal_list_with(usuario_model)
    def get(self):
        """Listar todos os usuários"""
        usuarios = Usuario.query.all()
        return usuarios

    @api.expect(usuario_model)
    @api.marshal_with(usuario_model, code=201)
    def post(self):
        """Cadastrar novo usuário"""
        dados = request.json
        novo = Usuario(nome=dados['nome'], email=dados['email'])
        db.session.add(novo)
        db.session.commit()
        return novo, 201


@api.route('/<int:id>')
@api.response(404, 'Usuário não encontrado')
@api.param('id', 'O identificador do usuário')
class UsuarioResource(Resource):
    @api.marshal_with(usuario_model)
    def get(self, id):
        """Buscar usuário por ID"""
        usuario = Usuario.query.get(id)
        if not usuario:
            api.abort(404, "Usuário não encontrado")
        return usuario

    @api.response(200, 'Usuário deletado com sucesso')
    def delete(self, id):
        """Deletar usuário por ID"""
        usuario = Usuario.query.get(id)
        if not usuario:
            api.abort(404, "Usuário não encontrado")
        db.session.delete(usuario)
        db.session.commit()
        return {'message': 'Usuário deletado com sucesso'}, 200
