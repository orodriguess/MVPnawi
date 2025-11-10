from flask_restx import Namespace, Resource, fields
from backend.utils.unidades import listar_unidades

api = Namespace('unidades', description='Lista de unidades padronizadas')

unidade_model = api.model('Unidade', {
    'codigo': fields.String(description='Símbolo da unidade (ex: g, kg, ml, m, un)'),
    'nome': fields.String(description='Nome completo da unidade'),
    'categoria': fields.String(description='Tipo de medida (peso, volume, etc.)'),
    'base': fields.String(description='Unidade base para conversão'),
    'fator': fields.Float(description='Fator multiplicativo para unidade base')
})

@api.route('/')
class UnidadesList(Resource):
    @api.marshal_list_with(unidade_model)
    def get(self):
        """Listar unidades disponíveis"""
        return listar_unidades()
