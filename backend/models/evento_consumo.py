# backend/models/evento_consumo.py
from backend.database.config import db
from datetime import datetime

class EventoConsumo(db.Model):
    __tablename__ = 'eventos_consumo'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    produto_base_id = db.Column(db.Integer, db.ForeignKey('produtos_base.id'), nullable=True)
    data_evento = db.Column(db.DateTime, default=datetime.utcnow)
    tipo_evento = db.Column(db.String(50))   # "compra", "uso", "reposição", "confirma_fim"
    quantidade = db.Column(db.Float, nullable=True)
    unidade = db.Column(db.String(10), nullable=True)
    origem = db.Column(db.String(50), default="manual")  # "manual", "estimado", "ocr"
    observacao = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "produto_base_id": self.produto_base_id,
            "data_evento": self.data_evento.isoformat(),
            "tipo_evento": self.tipo_evento,
            "quantidade": self.quantidade,
            "unidade": self.unidade,
            "origem": self.origem,
            "observacao": self.observacao
        }
