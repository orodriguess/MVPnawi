from flask_restx import Namespace, Resource, fields
from backend.utils.unidades import listar_unidades

api = Namespace("unidades", description="Listagem de unidades e conversões disponíveis")

unidade_model = api.model("Unidade", {
    "codigo": fields.String(required=True, description="Código da unidade (ex: g, kg, L, m, un)"),
    "nome": fields.String(required=True, description="Nome completo da unidade"),
    "categoria": fields.String(required=True, description="Categoria (peso, volume, comprimento, contagem)"),
    "base": fields.String(required=True, description="Unidade base para conversão"),
    "fator": fields.Float(required=True, description="Fator de conversão para a unidade base")
})


@api.route("/")
class UnidadeList(Resource):
    @api.marshal_list_with(unidade_model)
    def get(self):
        """Retorna todas as unidades disponíveis e suas relações"""
        return listar_unidades()
