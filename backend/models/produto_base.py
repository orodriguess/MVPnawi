# backend/models/produto_base.py
from backend.database.config import db
import json

class ProdutoBase(db.Model):
    __tablename__ = 'produtos_base'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    categoria = db.Column(db.String(50))
    unidade_principal = db.Column(db.String(20))
    tipo_calculo = db.Column(db.String(50))
    parametros_requeridos = db.Column(db.String(500), nullable=True)  # JSON string list

    consumo_medio_per_capita = db.Column(db.Float, nullable=True)
    unidade_referencia = db.Column(db.String(10), nullable=True)

    periodo_referencia_dias = db.Column(db.Integer, default=180)

    def get_parametros_requeridos(self):
        if not self.parametros_requeridos:
            return []
        try:
            return json.loads(self.parametros_requeridos)
        except Exception:
            return []

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "unidade_principal": self.unidade_principal,
            "tipo_calculo": self.tipo_calculo,
            "parametros_requeridos": self.get_parametros_requeridos(),
            "consumo_medio_per_capita": self.consumo_medio_per_capita,
            "unidade_referencia": self.unidade_referencia,
            "periodo_referencia_dias": self.periodo_referencia_dias
        }
