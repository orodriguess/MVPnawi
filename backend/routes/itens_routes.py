from flask_restx import Namespace, Resource, fields
from flask import request
from backend.database.config import db
from backend.models.item import Item

api = Namespace('itens', description='Gerenciamento de itens de consumo')

item_model = api.model('Item', {
    'id': fields.Integer(readonly=True, description='ID do item'),
    'nome': fields.String(required=True, description='Nome do item'),
    'categoria': fields.String(description='Categoria do item'),
    'quantidade_total': fields.Float(required=True, description='Quantidade total disponível'),
    'unidade': fields.String(description='Unidade de medida (ex: rolos, g, ml)'),
    'consumo_diario': fields.Float(required=True, description='Consumo médio diário'),
    'duracao_estimada': fields.Float(description='Duração estimada em dias')
})

@api.route('/')
class ItensList(Resource):
    @api.marshal_list_with(item_model)
    def get(self):
        """Listar todos os itens"""
        itens = Item.query.all()
        resultado = []
        for i in itens:
            data = {
                "id": i.id,
                "nome": i.nome,
                "categoria": i.categoria,
                "quantidade_total": i.quantidade_total,
                "unidade": i.unidade,
                "consumo_diario": i.consumo_diario,
                "duracao_estimada": i.calcular_duracao()
            }
            resultado.append(data)
        return resultado

    @api.expect(item_model)
    @api.marshal_with(item_model, code=201)
    def post(self):
        """Cadastrar novo item"""
        dados = request.json
        item = Item(
            nome=dados['nome'],
            categoria=dados.get('categoria'),
            quantidade_total=dados['quantidade_total'],
            unidade=dados.get('unidade'),
            consumo_diario=dados['consumo_diario']
        )
        db.session.add(item)
        db.session.commit()
        return item, 201


@api.route('/<int:id>')
@api.response(404, 'Item não encontrado')
class ItemResource(Resource):
    @api.marshal_with(item_model)
    def get(self, id):
        """Buscar item por ID"""
        item = Item.query.get(id)
        if not item:
            api.abort(404, "Item não encontrado")
        return item

    @api.response(200, 'Item deletado com sucesso')
    def delete(self, id):
        """Deletar item"""
        item = Item.query.get(id)
        if not item:
            api.abort(404, "Item não encontrado")
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deletado com sucesso'}, 200
