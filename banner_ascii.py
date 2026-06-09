"""Gerador de banner ASCII para o Mission Control AI."""

import argparse
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()


def exibir_banner_padrao():
    linha1 = pyfiglet.figlet_format("EnviroSat", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")

    console.print(Align.center(Text(linha1, style="bold #22c55e")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
             style="italic #8484A0")
    ))


def listar_fontes():
    fontes = pyfiglet.FigletFont.getFonts()
    console.print(f"[bold]Total de fontes disponíveis:[/bold] {len(fontes)}")
    for f in sorted(fontes)[:30]:
        console.print(f"  {f}")
    console.print("  ...")


def testar_fonte(font, text):
    try:
        resultado = pyfiglet.figlet_format(text, font=font)
        console.print(Text(resultado, style="bold #06B6D4"))
    except pyfiglet.FontNotFound:
        console.print(f"[red]Fonte '{font}' não encontrada.[/red]")


def demo_fontes():
    fontes_demo = ["ansi_shadow", "slant", "banner3", "big", "block", "digital", "doom", "standard"]
    for f in fontes_demo:
        console.print(f"\n[bold yellow]── Fonte: {f} ──[/bold yellow]")
        try:
            console.print(Text(pyfiglet.figlet_format("EnviroSat", font=f), style="#06B6D4"))
        except Exception:
            console.print(f"[red]Erro com fonte {f}[/red]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de banner ASCII")
    parser.add_argument("-fonts", action="store_true", help="Lista fontes disponíveis")
    parser.add_argument("-font", type=str, help="Testa uma fonte específica")
    parser.add_argument("-text", type=str, default="EnviroSat", help="Texto para renderizar")
    parser.add_argument("-demo", action="store_true", help="Demonstra 8 fontes")

    args = parser.parse_args()

    if args.fonts:
        listar_fontes()
    elif args.font:
        testar_fonte(args.font, args.text)
    elif args.demo:
        demo_fontes()
    else:
        exibir_banner_padrao()
