# backend/models/item_usuario.py
from backend.database.config import db
from datetime import datetime
import json

class ItemUsuario(db.Model):
    __tablename__ = 'itens_usuario'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    produto_base_id = db.Column(db.Integer, db.ForeignKey('produtos_base.id'), nullable=False)

    # parametros: livre (JSON) — ex: {"unidades":12,"metros_por_rolo":30,"consumo_diario":2}
    parametros = db.Column(db.Text, nullable=False)

    quantidade = db.Column(db.Float, nullable=True)  # valor agregado (opcional)
    unidade = db.Column(db.String(10), nullable=True)

    estoque_atual = db.Column(db.Float, nullable=True)
    consumo_estimado_diario = db.Column(db.Float, nullable=True)

    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_validade = db.Column(db.DateTime, nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    def get_parametros(self):
        try:
            return json.loads(self.parametros)
        except Exception:
            return {}

    def to_dict(self):
        p = self.get_parametros()
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "produto_base_id": self.produto_base_id,
            "parametros": p,
            "quantidade": self.quantidade,
            "unidade": self.unidade,
            "estoque_atual": self.estoque_atual,
            "consumo_estimado_diario": self.consumo_estimado_diario,
            "data_cadastro": self.data_cadastro.isoformat() if self.data_cadastro else None,
            "data_validade": self.data_validade.isoformat() if self.data_validade else None,
            "ativo": self.ativo
        }
