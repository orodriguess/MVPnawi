from backend.database.config import db
from backend.models.produto_base import ProdutoBase
from backend.app import app

def popular_produtos_base():
    produtos = [
        {"nome": "Papel Higiênico", "categoria": "Higiene", "unidade_principal": "m", "tipo_calculo": "papel_higienico"},
        {"nome": "Pasta de Dente", "categoria": "Higiene", "unidade_principal": "g", "tipo_calculo": "pasta_dente"},
        {"nome": "Sabonete", "categoria": "Higiene", "unidade_principal": "g", "tipo_calculo": "sabonete"},
        {"nome": "Café", "categoria": "Alimentação", "unidade_principal": "g", "tipo_calculo": "generico"}
    ]

    with app.app_context():
        for p in produtos:
            if not ProdutoBase.query.filter_by(nome=p["nome"]).first():
                novo = ProdutoBase(**p)
                db.session.add(novo)
        db.session.commit()
        print("✅ Produtos base inseridos com sucesso.")

if __name__ == "__main__":
    popular_produtos_base()
