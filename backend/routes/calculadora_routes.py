from flask_restx import Namespace, Resource, fields
from flask import request
from backend.models.produto_base import ProdutoBase
from backend.services.calculadora import calcular_duracao_item

api = Namespace("calculadora", description="Serviço de cálculo de duração de produtos")

# Modelo de entrada para Swagger
input_model = api.model("CalculoInput", {
    "produto_id": fields.Integer(required=True, description="ID do produto base"),
    "parametros": fields.Raw(required=True, description="Parâmetros específicos do produto"),
    "numero_pessoas": fields.Integer(default=1, description="Número de pessoas no domicílio")
})

@api.route("/")
class CalculadoraResource(Resource):
    @api.expect(input_model)
    def post(self):
        """
        Calcula a duração estimada de um produto conforme seus parâmetros.
        """
        data = request.json or {}
        produto_id = data.get("produto_id")
        parametros = data.get("parametros", {})
        numero_pessoas = data.get("numero_pessoas", 1)

        produto = ProdutoBase.query.get(produto_id)
        if not produto:
            return {"erro": f"Produto com id {produto_id} não encontrado"}, 404

        resultado = calcular_duracao_item(produto, parametros, numero_pessoas)
        return {"produto": produto.nome, **resultado}
