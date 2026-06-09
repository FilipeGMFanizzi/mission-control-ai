"""
Módulo de alertas e lógica de decisão — Trilha EnviroSat.
Toda a lógica de threshold fica aqui em Python, separada da IA.
"""


# Thresholds de cada parâmetro — valores definidos com base em operações reais
THRESHOLDS = {
    "sensor_termico": {
        "critico_alto": 70.0,    # sensor superaquecido — risco de dano permanente
        "alerta_alto": 50.0,     # temperatura elevada — atenção necessária
        "alerta_baixo": 10.0,    # temperatura muito baixa — possível falha criogênica
    },
    "sensor_optico": {
        "critico_baixo": 60.0,   # sensor com falha grave — imagens inutilizáveis
        "alerta_baixo": 75.0,    # degradação moderada — qualidade comprometida
    },
    "buffer_imagens": {
        "critico_alto": 90.0,    # buffer cheio — perda de dados iminente
        "alerta_alto": 75.0,     # buffer alto — priorizar downlink
    },
    "precisao_geo": {
        "critico_baixo": 70.0,   # geolocalização muito imprecisa — dados não confiáveis
        "alerta_baixo": 80.0,    # precisão baixa — alertas com localização duvidosa
    },
    "energia_disponivel": {
        "critico_baixo": 15.0,   # energia crítica — modo emergência obrigatório
        "alerta_baixo": 30.0,    # energia baixa — reduzir operações não essenciais
    },
}

# Níveis de severidade
CRITICO = "CRÍTICO"
ALERTA = "ALERTA"
NORMAL = "NORMAL"


def avaliar(dados: dict) -> list[dict]:
    """
    Recebe os dados de telemetria e retorna lista de alertas ativos.
    Cada alerta tem: parametro, nivel, valor, mensagem, acao_recomendada.
    """
    alertas = []

    # --- Sensor Térmico ---
    temp = dados["sensor_termico"]
    if temp > THRESHOLDS["sensor_termico"]["critico_alto"]:
        alertas.append({
            "parametro": "Sensor Térmico",
            "nivel": CRITICO,
            "valor": f"{temp}°C",
            "mensagem": "Superaquecimento crítico do sensor térmico.",
            "acao": "Desligar sensor imediatamente e acionar modo de resfriamento.",
        })
    elif temp > THRESHOLDS["sensor_termico"]["alerta_alto"]:
        alertas.append({
            "parametro": "Sensor Térmico",
            "nivel": ALERTA,
            "valor": f"{temp}°C",
            "mensagem": "Temperatura elevada no sensor térmico.",
            "acao": "Monitorar por 2 órbitas. Se persistir, reduzir carga operacional.",
        })
    elif temp < THRESHOLDS["sensor_termico"]["alerta_baixo"]:
        alertas.append({
            "parametro": "Sensor Térmico",
            "nivel": ALERTA,
            "valor": f"{temp}°C",
            "mensagem": "Temperatura abaixo do limite seguro.",
            "acao": "Verificar sistema de aquecimento e isolamento térmico.",
        })

    # --- Sensor Óptico ---
    optico = dados["sensor_optico"]
    if optico < THRESHOLDS["sensor_optico"]["critico_baixo"]:
        alertas.append({
            "parametro": "Sensor Óptico",
            "nivel": CRITICO,
            "valor": f"{optico}%",
            "mensagem": "Falha crítica no sensor óptico — imagens comprometidas.",
            "acao": "Suspender capturas. Acionar protocolo de diagnóstico do payload.",
        })
    elif optico < THRESHOLDS["sensor_optico"]["alerta_baixo"]:
        alertas.append({
            "parametro": "Sensor Óptico",
            "nivel": ALERTA,
            "valor": f"{optico}%",
            "mensagem": "Degradação moderada do sensor óptico.",
            "acao": "Aumentar redundância nas capturas. Checar calibração.",
        })

    # --- Buffer de Imagens ---
    buffer = dados["buffer_imagens"]
    if buffer > THRESHOLDS["buffer_imagens"]["critico_alto"]:
        alertas.append({
            "parametro": "Buffer de Imagens",
            "nivel": CRITICO,
            "valor": f"{buffer}%",
            "mensagem": "Buffer quase cheio — perda de dados iminente.",
            "acao": "Priorizar downlink na próxima janela disponível. Pausar novas capturas.",
        })
    elif buffer > THRESHOLDS["buffer_imagens"]["alerta_alto"]:
        alertas.append({
            "parametro": "Buffer de Imagens",
            "nivel": ALERTA,
            "valor": f"{buffer}%",
            "mensagem": "Buffer de imagens com ocupação alta.",
            "acao": "Agendar downlink prioritário na próxima passagem.",
        })

    # --- Precisão de Geolocalização ---
    geo = dados["precisao_geo"]
    if geo < THRESHOLDS["precisao_geo"]["critico_baixo"]:
        alertas.append({
            "parametro": "Precisão Geolocalização",
            "nivel": CRITICO,
            "valor": f"{geo}%",
            "mensagem": "Precisão geográfica crítica — alertas de foco podem estar errados.",
            "acao": "Suspender emissão de alertas para brigadas até recalibrar GPS.",
        })
    elif geo < THRESHOLDS["precisao_geo"]["alerta_baixo"]:
        alertas.append({
            "parametro": "Precisão Geolocalização",
            "nivel": ALERTA,
            "valor": f"{geo}%",
            "mensagem": "Precisão geográfica abaixo do ideal.",
            "acao": "Adicionar margem de erro nos alertas enviados ao INPE.",
        })

    # --- Energia ---
    energia = dados["energia_disponivel"]
    if energia < THRESHOLDS["energia_disponivel"]["critico_baixo"]:
        alertas.append({
            "parametro": "Energia Disponível",
            "nivel": CRITICO,
            "valor": f"{energia}%",
            "mensagem": "Energia em nível crítico — risco de desligamento.",
            "acao": "MODO EMERGÊNCIA ATIVADO: desligar sensores não essenciais. Manter só telemetria.",
        })
    elif energia < THRESHOLDS["energia_disponivel"]["alerta_baixo"]:
        alertas.append({
            "parametro": "Energia Disponível",
            "nivel": ALERTA,
            "valor": f"{energia}%",
            "mensagem": "Energia baixa.",
            "acao": "Reduzir frequência de capturas. Verificar painéis solares.",
        })

    # --- Focos de Calor (lógica combinada) ---
    focos = dados.get("focos_detectados", 0)
    if focos >= 8:
        alertas.append({
            "parametro": "Focos de Calor",
            "nivel": CRITICO,
            "valor": f"{focos} focos",
            "mensagem": f"Alto número de focos de calor detectados ({focos}) — possível incêndio em larga escala.",
            "acao": "Transmitir coordenadas ao INPE/IBAMA imediatamente. Acionar brigadas regionais.",
        })
    elif focos >= 4:
        alertas.append({
            "parametro": "Focos de Calor",
            "nivel": ALERTA,
            "valor": f"{focos} focos",
            "mensagem": f"{focos} focos de calor identificados na área de cobertura.",
            "acao": "Notificar INPE para análise. Aumentar resolução das capturas na região.",
        })

    return alertas


def nivel_geral(alertas: list[dict]) -> str:
    """
    Retorna o nível geral da missão com base nos alertas ativos.
    Se não tiver nenhum alerta, a missão está normal.
    """
    if not alertas:
        return NORMAL
    niveis = [a["nivel"] for a in alertas]
    if CRITICO in niveis:
        return CRITICO
    return ALERTA


def formatar_alertas(alertas: list[dict]) -> str:
    """Formata a lista de alertas em texto legível."""
    if not alertas:
        return "✅ Nenhum alerta ativo — todos os sistemas operando normalmente."

    linhas = []
    for a in alertas:
        icone = "🔴" if a["nivel"] == CRITICO else "🟡"
        linhas.append(f"{icone} [{a['nivel']}] {a['parametro']}: {a['valor']}")
        linhas.append(f"   ↳ {a['mensagem']}")
        linhas.append(f"   ➤ Ação: {a['acao']}")
        linhas.append("")

    return "\n".join(linhas).strip()
