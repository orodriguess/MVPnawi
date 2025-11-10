# backend/services/calculadora.py
from backend.utils.unidades import normalizar_valor
import math

def calcular_duracao_item(produto_base, parametros: dict, numero_pessoas: int = 1):
    """
    Retorna dict {duracao_dias: float | None, detalhes: {...}}
    produto_base: instância ProdutoBase
    parametros: dict com os campos informados pelo usuário (unidades, conteudo_por_unidade, consumo_diario, etc.)
    numero_pessoas: para aplicar consumo per-capita caso queira
    """
    tipo = (produto_base.tipo_calculo or "generico").lower()
    # exemplo comportamentos:
    try:
        if tipo in ("multiplicativo", "multiplicativo_simples", "papel_higienico"):
            # espera: unidades, conteudo_por_unidade, unidade_conteudo, consumo_diario, unidade_consumo
            unidades = float(parametros.get("unidades", 0))
            conteudo = float(parametros.get("conteudo_por_unidade", 0))
            consumo = float(parametros.get("consumo_diario", 0) or produto_base.consumo_medio_per_capita or 0)
            # normalizar: assumimos que conteudo e consumo já estão na mesma unidade base (frontend pode garantir)
            total = unidades * conteudo
            if consumo <= 0:
                return {"duracao_dias": None, "detalhes": {"total": total}}
            dias = total / (consumo * numero_pessoas)
            return {"duracao_dias": round(dias, 1), "detalhes": {"total": total}}
        elif tipo in ("consumo_direto", "generico"):
            quantidade_total = float(parametros.get("quantidade_total", parametros.get("total", 0) or 0))
            consumo = float(parametros.get("consumo_diario", 0) or produto_base.consumo_medio_per_capita or 0)
            if consumo <= 0:
                return {"duracao_dias": None, "detalhes": {"total": quantidade_total}}
            dias = quantidade_total / (consumo * numero_pessoas)
            return {"duracao_dias": round(dias, 1), "detalhes": {"total": quantidade_total}}
        elif tipo == "frequencia_por_unidade":
            unidades = float(parametros.get("unidades", 0))
            dias_por_unidade = float(parametros.get("dias_por_unidade", parametros.get("duracao_por_unidade", 1) or 1))
            dias = unidades * dias_por_unidade
            return {"duracao_dias": round(dias, 1), "detalhes": {}}
        else:
            # fallback genérico
            quantidade_total = float(parametros.get("quantidade_total", 0) or 0)
            consumo = float(parametros.get("consumo_diario", 0) or produto_base.consumo_medio_per_capita or 0)
            if consumo <= 0:
                return {"duracao_dias": None, "detalhes": {}}
            dias = quantidade_total / (consumo * numero_pessoas)
            return {"duracao_dias": round(dias, 1), "detalhes": {"total": quantidade_total}}
    except Exception as e:
        return {"duracao_dias": None, "detalhes": {"error": str(e)}}
