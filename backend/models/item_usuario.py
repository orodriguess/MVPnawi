from backend.database.config import db
from backend.models.produtos_base import ProdutoBase
from backend.utils.unidades import normalizar_valor

class ItemUsuario(db.Model):
    __tablename__ = "itens_usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    produto_base_id = db.Column(db.Integer, db.ForeignKey("produtos_base.id"), nullable=False)
    quantidade_total = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(10), nullable=False)
    pessoas = db.Column(db.Integer, default=1)
    dias_estimados = db.Column(db.Float, nullable=True)

    produto_base = db.relationship("ProdutoBase", backref=db.backref("itens_usuario", lazy=True))

    def calcular_duracao(self):
        """Calcula quanto tempo o item deve durar, com base na unidade e consumo médio."""
        produto = self.produto_base
        if not produto or not produto.consumo_medio_per_capita:
            return None

        # converte quantidade para unidade base
        quantidade_normalizada, unidade_base = normalizar_valor(self.quantidade_total, self.unidade)

        # só calcula se as unidades forem compatíveis
        if unidade_base != produto.unidade_referencia:
            raise ValueError(f"Incompatibilidade de unidade: {self.unidade} ≠ {produto.unidade_referencia}")

        consumo_total_diario = produto.consumo_medio_per_capita * self.pessoas
        if consumo_total_diario == 0:
            return None

        self.dias_estimados = round(quantidade_normalizada / consumo_total_diario, 1)
        return self.dias_estimados
