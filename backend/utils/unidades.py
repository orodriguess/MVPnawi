# backend/utils/unidades.py

CONVERSOES = {
    # --- Peso ---
    "mg": {"base": "g", "fator": 0.001, "categoria": "peso", "nome": "miligrama"},
    "g":  {"base": "g", "fator": 1, "categoria": "peso", "nome": "grama"},
    "kg": {"base": "g", "fator": 1000, "categoria": "peso", "nome": "quilograma"},

    # --- Volume ---
    "ml": {"base": "ml", "fator": 1, "categoria": "volume", "nome": "mililitro"},
    "L":  {"base": "ml", "fator": 1000, "categoria": "volume", "nome": "litro"},

    # --- Comprimento ---
    "cm": {"base": "m", "fator": 0.01, "categoria": "comprimento", "nome": "centímetro"},
    "m":  {"base": "m", "fator": 1, "categoria": "comprimento", "nome": "metro"},

    # --- Contagem ---
    "un": {"base": "un", "fator": 1, "categoria": "contagem", "nome": "unidade"}
}


def normalizar_valor(valor: float, unidade: str):
    """
    Converte o valor informado para sua unidade base.
    Exemplo: 1 kg -> 1000 g; 200 cm -> 2 m
    Retorna (valor_normalizado, unidade_base)
    """
    if unidade not in CONVERSOES:
        raise ValueError(f"Unidade '{unidade}' não reconhecida.")

    info = CONVERSOES[unidade]
    valor_base = valor * info["fator"]
    return round(valor_base, 4), info["base"]


def listar_unidades():
    """Retorna lista formatada de unidades disponíveis."""
    return [
        {
            "codigo": u,
            "nome": dados["nome"],
            "categoria": dados["categoria"],
            "base": dados["base"],
            "fator": dados["fator"]
        }
        for u, dados in CONVERSOES.items()
    ]
