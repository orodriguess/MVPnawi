# backend/routes/eventos_routes.py
from flask_restx import Namespace, Resource, fields
from backend.models.evento_consumo import EventoConsumo

api = Namespace('eventos', description='Eventos de consumo (logs)')

evento_model = api.model('Evento', {
    'id': fields.Integer,
    'usuario_id': fields.Integer,
    'produto_base_id': fields.Integer,
    'data_evento': fields.String,
    'tipo_evento': fields.String,
    'quantidade': fields.Float,
    'unidade': fields.String,
    'origem': fields.String,
    'observacao': fields.String
})

@api.route('/')
class EventosList(Resource):
    @api.marshal_list_with(evento_model)
    def get(self):
        eventos = EventoConsumo.query.order_by(EventoConsumo.data_evento.desc()).limit(200).all()
        return [e.to_dict() for e in eventos]
