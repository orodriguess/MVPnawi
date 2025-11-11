# backend/database/seed_produtos.py
from backend.app import app
from backend.database.config import db
from backend.models.produtos_base import ProdutoBase
import json

def seed():
    produtos = [
        {
            "nome": "Papel Higiênico",
            "categoria": "Higiene",
            "unidade_principal": "m",
            "tipo_calculo": "multiplicativo",
            "parametros_requeridos": ["unidades","conteudo_por_unidade","consumo_diario"],
            "consumo_medio_per_capita": 2.0,
            "unidade_referencia": "m",
            "periodo_referencia_dias": 180
        },
        {
            "nome": "Pasta de Dente",
            "categoria": "Higiene",
            "unidade_principal": "g",
            "tipo_calculo": "multiplicativo",
            "parametros_requeridos": ["unidades","conteudo_por_unidade","consumo_diario"],
            "consumo_medio_per_capita": 1.5,
            "unidade_referencia": "g",
            "periodo_referencia_dias": 180
        },
        {
            "nome": "Sabonete",
            "categoria": "Higiene",
            "unidade_principal": "un",
            "tipo_calculo": "frequencia_por_unidade",
            "parametros_requeridos": ["unidades","dias_por_unidade"],
            "consumo_medio_per_capita": 0.05,
            "unidade_referencia": "un",
            "periodo_referencia_dias": 180
        },
        {
            "nome": "Café",
            "categoria": "Alimentação",
            "unidade_principal": "g",
            "tipo_calculo": "consumo_direto",
            "parametros_requeridos": ["quantidade_total","consumo_diario"],
            "consumo_medio_per_capita": 20.0,
            "unidade_referencia": "g",
            "periodo_referencia_dias": 180
        }
    ]

    with app.app_context():
        for p in produtos:
            existente = ProdutoBase.query.filter_by(nome=p["nome"]).first()
            if not existente:
                pb = ProdutoBase(
                    nome=p["nome"],
                    categoria=p["categoria"],
                    unidade_principal=p["unidade_principal"],
                    tipo_calculo=p["tipo_calculo"],
                    parametros_requeridos=json.dumps(p["parametros_requeridos"]),
                    consumo_medio_per_capita=p["consumo_medio_per_capita"],
                    unidade_referencia=p["unidade_referencia"],
                    periodo_referencia_dias=p["periodo_referencia_dias"]
                )
                db.session.add(pb)
        db.session.commit()
        print("✅ seed_produtos finalizado.")
