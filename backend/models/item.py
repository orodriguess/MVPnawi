from backend.database.config import db

class Item(db.Model):
    __tablename__ = 'itens'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))
    quantidade_total = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(20))
    consumo_diario = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    def calcular_duracao(self):
        """Retorna a duração estimada do item em dias"""
        if self.consumo_diario <= 0:
            return None
        dias = self.quantidade_total / self.consumo_diario
        return round(dias, 1)
