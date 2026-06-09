"""
Motor de análise da Mission Control AI — Trilha EnviroSat.
Aqui fica a lógica que amarra telemetria + alertas + IA.
"""

import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path

from src import telemetria, alertas

load_dotenv()

TRILHA = "envirosat"

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")}
)


def llm(prompt: str, system: str = None, max_tokens: int = 800, temperature: float = 0.3) -> str:
    """Envia prompt ao gpt-oss:120b via Ollama Cloud e retorna a resposta."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        resposta = client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False,
        )
        return resposta["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"


def load_system_prompt() -> str:
    """Carrega o system prompt do arquivo prompts/system_prompt.md."""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    # fallback básico caso o arquivo não exista
    return (
        "Você é ARIA, analista de IA do EnviroSat-1. "
        "Interprete dados de telemetria e conecte anomalias ao impacto ambiental no Brasil."
    )


class MissionEngine:
    """Motor central do sistema — integra telemetria, alertas e IA."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self._ultima_telemetria: dict | None = None
        self._ultimos_alertas: list[dict] = []

    def is_ready(self) -> bool:
        return True

    def status_snapshot(self) -> str:
        """Retorna um resumo textual do estado atual da missão."""
        dados = telemetria.coletar()
        self._ultima_telemetria = dados
        lista_alertas = alertas.avaliar(dados)
        self._ultimos_alertas = lista_alertas

        nivel = alertas.nivel_geral(lista_alertas)
        icone_nivel = "🔴" if nivel == "CRÍTICO" else ("🟡" if nivel == "ALERTA" else "🟢")

        texto_telemetria = telemetria.formatar_leitura(dados)
        texto_alertas = alertas.formatar_alertas(lista_alertas)

        return (
            f"{texto_telemetria}\n\n"
            f"{icone_nivel} Status geral da missão: {nivel}\n\n"
            f"── Alertas Ativos ──\n{texto_alertas}"
        )

    def analyze(self, pergunta_usuario: str) -> str:
        """
        Analisa a pergunta do usuário com base na telemetria atual + alertas + IA.
        Injeta os dados reais no prompt antes de chamar o modelo.
        """
        # Coleta telemetria fresca
        dados = telemetria.coletar()
        self._ultima_telemetria = dados

        # Avalia alertas via lógica Python
        lista_alertas = alertas.avaliar(dados)
        self._ultimos_alertas = lista_alertas
        nivel = alertas.nivel_geral(lista_alertas)

        # Formata contexto para injetar no prompt
        texto_telemetria = telemetria.formatar_leitura(dados)
        texto_alertas = alertas.formatar_alertas(lista_alertas)

        # Pega histórico das últimas leituras pra dar contexto temporal à IA
        historico = telemetria.get_historico()
        contexto_historico = ""
        if len(historico) > 1:
            leituras_anteriores = historico[:-1]  # todas menos a atual
            energia_media = sum(h["energia_disponivel"] for h in leituras_anteriores) / len(leituras_anteriores)
            temp_media = sum(h["sensor_termico"] for h in leituras_anteriores) / len(leituras_anteriores)
            contexto_historico = (
                f"\n\n📊 Contexto histórico (últimas {len(leituras_anteriores)} leituras):\n"
                f"  Energia média anterior: {energia_media:.1f}%\n"
                f"  Temperatura média anterior: {temp_media:.1f}°C"
            )

        # Monta o prompt completo com todos os dados injetados
        prompt = f"""
Dados atuais de telemetria do EnviroSat-1:

{texto_telemetria}
{contexto_historico}

Status geral da missão: {nivel}

Alertas ativos:
{texto_alertas}

---
Pergunta do operador: {pergunta_usuario}

Responda com base nos dados acima. Conecte a análise técnica ao impacto ambiental real.
"""

        return llm(prompt, system=self.system_prompt)
