import time
from utils import data_manager, simulador
from . import menu

def medir_tempo(func, *args, **kwargs):
    inicio = time.perf_counter()
    resultado = func(*args, **kwargs)
    fim = time.perf_counter()
    tempo_ms = (fim - inicio) * 1000
    tempo_formatado = f"{tempo_ms:.2f}".replace(".", ",")
    return resultado, tempo_formatado

def regenerate_data():
    """Opção 7: Regenerar Dados Simulados"""
    num_registros = menu.ask_input_int("📊 Quantos registros deseja gerar?", default=50)
    if num_registros is None:
        num_registros = 50
    menu.show_message("🔄 Regenerando dados simulados...", "bold purple")
    dados_simulados = simulador.generate_data(num_registros)
    data_manager.save_data(dados_simulados)

    menu.show_message(
        "✅ Dados simulados regenerados com sucesso!",
        "bold green",
    )
    return dados_simulados


def system_settings():
    """Opção 8: Configurações do Sistema"""
    menu.show_message("👷 Em construção: Configurações do Sistema", "bold yellow")


def exit_system():
    """Opção 9: Sair"""
    menu.show_message("👋 Saindo do sistema. Até logo!", "bold magenta")
