# backend/routes/itens_usuario_routes.py
from flask_restx import Namespace, Resource, fields
from flask import request
from backend.database.config import db
from backend.models.item_usuario import ItemUsuario
from backend.models.evento_consumo import EventoConsumo
from backend.models.produto_base import ProdutoBase
from backend.services.calculadora import calcular_duracao_item 

api = Namespace('itens_usuario', description='Itens do usuário (estoque e parâmetros)')

item_model = api.model('ItemUsuario', {
    'id': fields.Integer(readonly=True),
    'usuario_id': fields.Integer,
    'produto_base_id': fields.Integer(required=True),
    'parametros': fields.Raw(required=True, description='JSON com parâmetros específicos'),
    'estoque_atual': fields.Float,
    'consumo_estimado_diario': fields.Float
})

@api.route('/')
class ItensUsuarioList(Resource):
    @api.marshal_list_with(item_model)
    def get(self):
        itens = ItemUsuario.query.all()
        return [i.to_dict() for i in itens]

    @api.expect(item_model)
    def post(self):
        dados = request.json
        parametros = dados.get('parametros', {})
        import json
        item = ItemUsuario(
            usuario_id=dados.get('usuario_id'),
            produto_base_id=dados['produto_base_id'],
            parametros=json.dumps(parametros),
            estoque_atual=dados.get('estoque_atual'),
            consumo_estimado_diario=dados.get('consumo_estimada_diaria') or None
        )
        db.session.add(item)
        db.session.commit()

        # cria evento de compra/registro
        ev = EventoConsumo(
            usuario_id=item.usuario_id,
            produto_base_id=item.produto_base_id,
            tipo_evento='compra',
            quantidade=item.estoque_atual,
            unidade=item.unidade or None,
            origem='manual',
            observacao='Registro inicial do item'
        )
        db.session.add(ev)
        db.session.commit()

        # opcional: calcular duracao usando calculadora (se implementada)
        try:
            produto = ProdutoBase.query.get(item.produto_base_id)
            duracao = calcular_duracao_item(produto, parametros)
            # aqui não gravamos duracao fixa, mas o front pode exibir com GET /itens_usuario
        except Exception:
            pass

        return item.to_dict(), 201

@api.route('/<int:id>')
class ItemUsuarioResource(Resource):
    def get(self, id):
        item = ItemUsuario.query.get(id)
        if not item:
            api.abort(404, "Item não encontrado")
        return item.to_dict()

    def delete(self, id):
        item = ItemUsuario.query.get(id)
        if not item:
            api.abort(404, "Item não encontrado")
        db.session.delete(item)
        db.session.commit()
        # registra evento de remoção
        ev = EventoConsumo(
            produto_base_id=item.produto_base_id,
            tipo_evento='remocao',
            origem='manual',
            observacao=f'Item {id} removido'
        )
        db.session.add(ev)
        db.session.commit()
        return {'message': 'Item removido'}, 200

# rota para confirmar que item acabou (gera evento 'confirma_fim')
@api.route('/<int:id>/confirma_fim')
class ItemConfirmaFim(Resource):
    def post(self, id):
        item = ItemUsuario.query.get(id)
        if not item:
            api.abort(404, "Item não encontrado")
        ev = EventoConsumo(
            usuario_id=item.usuario_id,
            produto_base_id=item.produto_base_id,
            tipo_evento='confirma_fim',
            quantidade=0,
            unidade=item.unidade,
            origem='manual',
            observacao='Usuário confirmou fim do item'
        )
        db.session.add(ev)
        item.ativo = False
        db.session.commit()
        return {'message': 'Confirmado fim do item, evento registrado'}, 200
