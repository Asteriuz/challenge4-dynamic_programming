import time
from core import busca, ordenacao, dp
from ui import config
from utils import data_manager, simulador

from . import menu


def medir_tempo(func, *args, **kwargs):
    inicio = time.perf_counter()
    resultado = func(*args, **kwargs)
    fim = time.perf_counter()
    tempo_ms = (fim - inicio) * 1000
    tempo_formatado = f"{tempo_ms:.2f}".replace(".", ",")
    return resultado, tempo_formatado


def view_data_queue(fila):
    """Opção 1: Visualizar Consumo (Fila - Cronológico)"""
    menu.show_data(fila.get_all(), "Consumo em Ordem Cronológica (FIFO - Fila)")


def view_data_stack(pilha):
    """Opção 2: Visualizar Consumo (Pilha - Inverso)"""
    menu.show_data(pilha.get_all(), "Últimos Consumos (LIFO - Pilha)")


def search_fuzzy(dados_consumo, max_dist=2):
    """Opção: Buscar Insumo (Fuzzy Search)"""
    nome_insumo = menu.ask_input("🔍 Digite o nome aproximado do insumo a buscar")
    if not nome_insumo: # type: ignore
        menu.show_message("❌ Nome do insumo não pode ser vazio.", "bold red")
        return

    # Versão iterativa
    resultado_iter, tempo_iter = medir_tempo(
        lambda dados, chave, termo: dp.busca_fuzzy_iter(
            dados, chave, termo, max_dist=max_dist
        ),
        dados_consumo,
        "nome_insumo",
        nome_insumo,
    )

    # Versão recursiva
    resultado_rec, tempo_rec = medir_tempo(
        lambda dados, chave, termo: dp.busca_fuzzy_rec(dados, chave, termo, max_dist=max_dist),
        dados_consumo,
        "nome_insumo",
        nome_insumo,
    )

    if resultado_iter:
        menu.show_data(
            resultado_iter,
            f"Resultado da Busca Fuzzy Iterativa por '{nome_insumo}' (⏱️  Tempo: {tempo_iter}ms)",
        )
    else:
        menu.show_message(
            f"❌ Nenhum insumo semelhante a '{nome_insumo}' encontrado (Iterativo).",
            "bold red",
        )

    if resultado_rec:
        menu.show_data(
            resultado_rec,
            f"Resultado da Busca Fuzzy Recursiva por '{nome_insumo}' (⏱️  Tempo: {tempo_rec}ms)",
        )
    else:
        menu.show_message(
            f"❌ Nenhum insumo semelhante a '{nome_insumo}' encontrado (Recursivo).",
            "bold red",
        )

    if not resultado_iter and not resultado_rec:
        tentar_novamente = menu.ask_input(
            "Nenhum resultado encontrado. Deseja tentar novamente?", choices=["s", "n"], default="S"
        )
        print()
        if tentar_novamente.lower() == "s": # type: ignore
            search_fuzzy(dados_consumo)


def search_sequential(dados_consumo):
    """Opção 4: Buscar Insumo (Busca Sequencial)"""
    nome_insumo = menu.ask_input("🔍 Digite o nome do insumo a buscar")
    resultado, tempo_busca_formatado = medir_tempo(
        busca.busca_sequencial, dados_consumo, "nome_insumo", nome_insumo
    )
    if resultado:
        menu.show_data(
            resultado,
            f"Resultado da Busca Sequencial por '{nome_insumo}' (⏱️  Tempo: {tempo_busca_formatado}ms)",
        )
    else:
        menu.show_message(f"❌ Insumo '{nome_insumo}' não encontrado.", "bold red")


def search_binary(dados_consumo):
    """Opção 5: Buscar Insumo (Busca Binária)"""
    menu.show_message(
        "ℹ️  Para a busca binária, a lista será ordenada por nome.", "bold cyan"
    )
    # A busca binária exige uma lista ordenada
    dados_ordenados = sorted(dados_consumo, key=lambda x: x["nome_insumo"])
    nome_insumo = menu.ask_input("🔍 Digite o nome do insumo a buscar")
    resultado, tempo_busca_formatado = medir_tempo(
        busca.busca_binaria, dados_ordenados, "nome_insumo", nome_insumo
    )
    if resultado:
        menu.show_data(
            resultado,
            f"Resultado da Busca Binária por '{nome_insumo}' (⏱️  Tempo: {tempo_busca_formatado}ms)",
        )
    else:
        menu.show_message(f"❌ Insumo '{nome_insumo}' não encontrado.", "bold red")


def sort_merge(dados_consumo):
    """Opção 6: Ordenação (Merge Sort)"""
    _sort_data(dados_consumo, "Merge Sort", ordenacao.merge_sort)


def sort_quick(dados_consumo):
    """Opção 7: Ordenação (Quick Sort)"""
    _sort_data(dados_consumo, "Quick Sort", ordenacao.quick_sort)


def _sort_data(dados_consumo, algoritmo, sort_function):
    """Função auxiliar para ordenação"""
    menu.show_message(f"📈 Ordenando com [bold]{algoritmo}[/bold]...", "yellow")

    chave_menu = {
        "1": ("id_insumo", "🆔 ID do Insumo"),
        "2": ("nome_insumo", "🧪 Nome do Insumo"),
        "3": ("lote", "📦 Lote"),
        "4": ("quantidade_consumida", "📊 Quantidade Consumida"),
        "5": ("data_consumo", "📅 Data de Consumo"),
        "6": ("validade", "⏰ Validade"),
    }

    opcoes_texto = "\n".join([f"[{k}] {v[1]}" for k, v in chave_menu.items()])
    menu.show_message(
        f"[bold]Escolha o campo para ordenação:[/bold]\n{opcoes_texto}",
        "white",
        new_line_start=False,
    )

    chave_ordenacao = menu.ask_input(
        "Digite o número da opção desejada",
        choices=list(chave_menu.keys()),
    )
    chave, _ = chave_menu.get(chave_ordenacao, ("id_insumo", "ID do Insumo")) # type: ignore

    dados_ordenados, tempo_ordenacao_formatado = medir_tempo(
        sort_function, dados_consumo, chave
    )
    titulo = f"Insumos Ordenados por '{chave}' usando {algoritmo} (⏱️  Tempo: {tempo_ordenacao_formatado}ms)"
    menu.show_data(dados_ordenados, titulo)


def regenerate_data():
    """Opção 8: Regenerar Dados Simulados"""
    num_registros = menu.ask_input_int("📊 Quantos registros deseja gerar?", default=50)
    menu.show_message("🔄 Regenerando dados simulados...", "bold purple")
    dados_simulados = simulador.generate_data(num_registros)  # type: ignore
    data_manager.save_data(dados_simulados)

    # Return the new data so main can update its variables
    menu.show_message(
        "✅ Dados simulados regenerados com sucesso!",
        "bold green",
    )
    return dados_simulados


def system_settings(config_manager):
    """Opção 9: Configurações do Sistema"""
    config.config_menu(config_manager)


def exit_system():
    """Opção 10: Sair"""
    menu.show_message("👋 Saindo do sistema. Até logo!", "bold magenta")
