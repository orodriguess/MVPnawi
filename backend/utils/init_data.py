# backend/utils/init_data.py
from backend.models import ProdutoBase
from backend.database.config import db

def popular_dados_iniciais():
    """Popula o banco com produtos básicos na primeira execução."""
    if ProdutoBase.query.first():
        return

    produtos_iniciais = [
        ProdutoBase(
            nome="Papel Higiênico",
            categoria="higiene",
            unidade_principal="m",  # metros
            tipo_calculo="comprimento_por_pessoa",
            parametros_requeridos="rolos, metros_por_rolo",
            consumo_medio_per_capita=2.5,  # metros/dia
            unidade_referencia="m",
            periodo_referencia_dias=30
        ),
        ProdutoBase(
            nome="Pasta de Dente",
            categoria="higiene",
            unidade_principal="g",  # gramas
            tipo_calculo="peso_por_pessoa",
            parametros_requeridos="tubos, gramas_por_tubo",
            consumo_medio_per_capita=2.0,  # g/dia
            unidade_referencia="g",
            periodo_referencia_dias=30
        ),
        ProdutoBase(
            nome="Sabonete",
            categoria="higiene",
            unidade_principal="un",  # unidade
            tipo_calculo="unidades_por_pessoa",
            parametros_requeridos="barras",
            consumo_medio_per_capita=0.15,  # un/dia (~1 por semana)
            unidade_referencia="un",
            periodo_referencia_dias=30
        ),
        ProdutoBase(
            nome="Café em pó",
            categoria="alimentação",
            unidade_principal="g",  # gramas
            tipo_calculo="peso_por_pessoa",
            parametros_requeridos="gramas_disponiveis",
            consumo_medio_per_capita=15,  # g/dia
            unidade_referencia="g",
            periodo_referencia_dias=30
        ),
    ]

    db.session.add_all(produtos_iniciais)
    db.session.commit()
    print("✅ Dados iniciais de produtos_base atualizados com unidades principais!")
