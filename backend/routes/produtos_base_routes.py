from flask_restx import Namespace, Resource, fields
from backend.models.produto_base import ProdutoBase

api = Namespace('produtos_base', description='Lista de produtos suportados')

produto_base_model = api.model('ProdutoBase', {
    'id': fields.Integer,
    'nome': fields.String,
    'categoria': fields.String,
    'unidade_principal': fields.String,
    'tipo_calculo': fields.String
})

@api.route('/')
class ProdutosBaseList(Resource):
    @api.marshal_list_with(produto_base_model)
    def get(self):
        """Listar produtos suportados"""
        produtos = ProdutoBase.query.all()
        return produtos
