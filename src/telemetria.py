"""
Módulo de telemetria simulada — Trilha EnviroSat.
Simula dados de um satélite de observação ambiental tipo Amazônia-1.
"""

import random
from datetime import datetime


# Faixas normais de operação para cada parâmetro
FAIXAS_NORMAIS = {
    "sensor_termico": (15.0, 45.0),       # temperatura do sensor térmico (°C)
    "sensor_optico": (80.0, 100.0),        # saúde do sensor óptico RGB+NIR (%)
    "buffer_imagens": (0.0, 75.0),         # buffer de imagens não transmitidas (%)
    "precisao_geo": (85.0, 100.0),         # precisão de geolocalização (%)
    "energia_disponivel": (30.0, 100.0),   # energia disponível nos painéis solares (%)
}

# Histórico das últimas leituras (simula memória de contexto)
_historico: list[dict] = []


def coletar() -> dict:
    """
    Gera uma leitura simulada de telemetria do satélite.
    Às vezes injeta valores fora da faixa normal pra deixar o sistema interessante.
    Retorna um dicionário com todos os parâmetros + timestamp.
    """
    # 25% de chance de simular alguma anomalia em algum sensor
    anomalia = random.random() < 0.25

    dados = {}

    for parametro, (minimo, maximo) in FAIXAS_NORMAIS.items():
        if anomalia and random.random() < 0.4:
            # Gera valor fora da faixa — pode ser alto ou baixo demais
            if random.random() < 0.5:
                valor = round(random.uniform(maximo * 1.1, maximo * 1.5), 2)
            else:
                valor = round(random.uniform(minimo * 0.1, minimo * 0.6), 2)
        else:
            valor = round(random.uniform(minimo, maximo), 2)

        dados[parametro] = valor

    dados["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dados["orbita_numero"] = random.randint(1200, 9999)
    dados["focos_detectados"] = random.randint(0, 12) if dados["sensor_termico"] > 50 else random.randint(0, 2)

    # Salva no histórico (mantém só os últimos 5)
    _historico.append(dados)
    if len(_historico) > 5:
        _historico.pop(0)

    return dados


def get_historico() -> list[dict]:
    """Retorna as últimas leituras coletadas (máximo 5)."""
    return list(_historico)


def formatar_leitura(dados: dict) -> str:
    """
    Formata os dados de telemetria em texto legível para exibir no terminal
    ou injetar no prompt da IA.
    """
    linhas = [
        f"📡 TELEMETRIA EnviroSat — Órbita #{dados['orbita_numero']}",
        f"🕐 Timestamp: {dados['timestamp']}",
        "─" * 45,
        f"🌡️  Sensor Térmico:        {dados['sensor_termico']}°C",
        f"📷  Saúde Sensor Óptico:   {dados['sensor_optico']}%",
        f"💾  Buffer de Imagens:     {dados['buffer_imagens']}%",
        f"📍  Precisão Geoloc.:      {dados['precisao_geo']}%",
        f"⚡  Energia Disponível:    {dados['energia_disponivel']}%",
        f"🔥  Focos Detectados:      {dados['focos_detectados']} focos",
    ]
    return "\n".join(linhas)
