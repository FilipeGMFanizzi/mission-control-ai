"""
Interface CLI estilo Claude Code — usa Rich + prompt-toolkit.
Trilha: EnviroSat — Mission Control AI.
"""

import pyfiglet
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#22c55e bold"}))


def show_banner():
    """Exibe banner ASCII colorido e painel de boas-vindas."""
    banner1 = pyfiglet.figlet_format("EnviroSat", font="ansi_shadow")
    banner2 = pyfiglet.figlet_format("Mission Control", font="small")

    console.print(Align.center(Text(banner1, style="bold #22c55e")))
    console.print(Align.center(Text(banner2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──\n", style="italic #8484A0")
    ))

    tabela = Table(show_header=False, box=None, padding=(0, 2))
    tabela.add_column(style="#8484A0")
    tabela.add_column(style="white")
    tabela.add_row("Modelo", "gpt-oss:120b via Ollama Cloud")
    tabela.add_row("Trilha", "🌳 EnviroSat — Observação Ambiental")
    tabela.add_row("Satélite", "EnviroSat-1 (simulado)")
    tabela.add_row("Comandos", "/help  /status  /about  /clear  /exit")

    console.print(Panel(
        tabela,
        title="[bold #06B6D4]◆ MISSION CONTROL AI[/bold #06B6D4]",
        border_style="#06B6D4",
        padding=(1, 2),
    ))
    console.print()


def show_response(text: str, titulo: str = "◆ ARIA — EnviroSat-1"):
    """Renderiza a resposta da IA em painel com timestamp."""
    agora = datetime.now().strftime("%H:%M:%S")
    console.print(Panel(
        text,
        title=f"[bold #22c55e]{titulo}[/bold #22c55e]",
        subtitle=f"[#8484A0]{agora}[/#8484A0]",
        border_style="#22c55e",
        padding=(1, 2),
    ))
    console.print()


def show_about():
    """Exibe informações sobre o projeto."""
    texto = (
        "[bold]EnviroSat Mission Control AI[/bold]\n\n"
        "Sistema de monitoramento inteligente de missão espacial desenvolvido\n"
        "para a Global Solution 2026.1 da FIAP — Curso de Ciência da Computação.\n\n"
        "[bold]Trilha:[/bold] 🌳 EnviroSat — Observação Ambiental\n"
        "[bold]Satélite simulado:[/bold] Satélite de observação ambiental com sensor térmico\n"
        "e óptico, similar ao Amazônia-1 operado pelo INPE.\n\n"
        "[bold]Impacto terrestre:[/bold]\n"
        "Dados deste satélite alimentam o sistema DETER do INPE, usado para emissão\n"
        "de alertas de desmatamento e incêndios que orientam brigadas do IBAMA.\n\n"
        "[bold]Stack:[/bold] Python 3.10+ · Ollama Cloud · Rich · prompt-toolkit"
    )
    console.print(Panel(
        texto,
        title="[bold #06B6D4]◆ Sobre o Projeto[/bold #06B6D4]",
        border_style="#06B6D4",
        padding=(1, 2),
    ))
    console.print()


def show_help():
    """Exibe tabela de comandos disponíveis."""
    tabela = Table(title="Comandos disponíveis", border_style="#06B6D4", header_style="bold #06B6D4")
    tabela.add_column("Comando", style="#22c55e bold", width=12)
    tabela.add_column("Descrição", style="white")

    tabela.add_row("/status", "Coleta telemetria atual e exibe status completo da missão")
    tabela.add_row("/about", "Informações sobre o projeto e a trilha EnviroSat")
    tabela.add_row("/clear", "Limpa o terminal e reexibe o banner")
    tabela.add_row("/help", "Exibe esta tabela de comandos")
    tabela.add_row("/exit", "Encerra o sistema")
    tabela.add_row("[pergunta]", "Qualquer texto é enviado à IA com dados de telemetria injetados")

    console.print(tabela)
    console.print()


def run_cli(engine):
    """Loop principal da CLI."""
    show_banner()

    if not engine.is_ready():
        console.print(
            "  ⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n",
            style="bold yellow"
        )

    while True:
        try:
            user_input = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[#8484A0]Encerrando Mission Control AI...[/#8484A0]")
            break

        if not user_input:
            continue

        if user_input.lower() == "/exit":
            console.print("\n[#8484A0]Encerrando Mission Control AI. Até logo.[/#8484A0]\n")
            break

        elif user_input.lower() == "/help":
            show_help()

        elif user_input.lower() == "/about":
            show_about()

        elif user_input.lower() == "/clear":
            console.clear()
            show_banner()

        elif user_input.lower() == "/status":
            console.print("\n[#8484A0]Coletando telemetria...[/#8484A0]")
            snapshot = engine.status_snapshot()
            show_response(snapshot, titulo="◆ Status da Missão")

        else:
            console.print("\n[#8484A0]Analisando com ARIA...[/#8484A0]")
            resposta = engine.analyze(user_input)
            show_response(resposta)
