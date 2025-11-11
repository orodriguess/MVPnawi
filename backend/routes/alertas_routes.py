from flask_restx import Namespace, Resource, fields
from backend.database.config import db
from backend.models.item_usuario import ItemUsuario
from backend.models.produtos_base import ProdutoBase
from datetime import datetime, timedelta

api = Namespace("alertas", description="Gera alertas de consumo próximo do fim")

alerta_model = api.model("Alerta", {
    "produto": fields.String(required=True, description="Nome do produto"),
    "quantidade_atual": fields.Float(required=True, description="Quantidade atual em estoque"),
    "unidade": fields.String(required=True, description="Unidade principal"),
    "dias_restantes": fields.Float(required=True, description="Dias restantes até acabar"),
    "data_estimativa_fim": fields.String(description="Data estimada do fim do estoque")
})


@api.route("/")
class AlertasResource(Resource):
    @api.marshal_list_with(alerta_model)
    def get(self):
        """Retorna produtos próximos de acabar"""
        itens = ItemUsuario.query.all()
        alertas = []

        for item in itens:
            produto = ProdutoBase.query.get(item.produto_base_id)
            if not produto:
                continue

            consumo_diario = item.consumo_medio_diario or 0
            if consumo_diario <= 0:
                continue

            dias_restantes = item.quantidade_estoque / consumo_diario
            if dias_restantes < 10:  # 🔸 threshold de alerta
                data_fim = (datetime.now() + timedelta(days=dias_restantes)).strftime("%d/%m/%Y")

                alertas.append({
                    "produto": produto.nome,
                    "quantidade_atual": item.quantidade_estoque,
                    "unidade": produto.unidade_principal,
                    "dias_restantes": round(dias_restantes, 1),
                    "data_estimativa_fim": data_fim
                })

        return alertas
