from ui import menu, menu_logic
from utils import data_manager, simulador
from utils.config.config_manager import ConfigManager
from core import fila_pilha
import sys

MENU_CONFIG = {
    "panel_title": "[bold magenta]🏥 Gerenciador de Insumos de Diagnóstico[/bold magenta]",
    "panel_border_style": "bold cyan",
    "groups": [
        {
            "title": "📊 VISUALIZAÇÃO DE DADOS",
            "color": "purple",
            "options": [
                {
                    "number": 1,
                    "description": "Visualizar Consumo (Fila - Cronológico)",
                },
                {
                    "number": 2,
                    "description": "Visualizar Consumo (Pilha - Inverso)",
                },
            ],
        },
        {
            "title": "🔍 BUSCA DE INSUMOS",
            "color": "green",
            "options": [
                {
                    "number": 3,
                    "description": "Buscar Insumo (Fuzzy Search)",
                },
                {
                    "number": 4,
                    "description": "Buscar Insumo (Busca Sequencial)",
                },
                {
                    "number": 5,
                    "description": "Buscar Insumo (Busca Binária)",
                },
            ],
        },
        {
            "title": "📈 ORDENAÇÃO POR CONSUMO/VALIDADE",
            "color": "yellow",
            "options": [
                {
                    "number": 6,
                    "description": "(Merge Sort)",
                },
                {
                    "number": 7,
                    "description": "(Quick Sort)",
                },
            ],
        },
        {
            "title": "🔧 GERENCIAMENTO",
            "color": "cyan",
            "options": [
                {
                    "number": 8,
                    "description": "Regenerar Dados Simulados",
                },
                {
                    "number": 9,
                    "description": "Configurações do Sistema",
                },
            ],
        },
        {
            "title": "🚪 SISTEMA",
            "color": "red",
            "options": [
                {
                    "number": 10,
                    "description": "Sair",
                },
            ],
        },
    ],
}


def main():
    """Função principal que executa o loop da aplicação."""
    dados_consumo = data_manager.load_data()
    config = ConfigManager()

    if not dados_consumo:
        menu.console.print(
            "[bold yellow]Atenção:[/bold yellow] O arquivo 'data/consumo.json' está vazio ou não foi encontrado."
        )
        resposta = menu.ask_input(
            "Deseja gerar dados simulados automaticamente?", choices=["s", "n"]
        )

        if resposta.lower() == "s":  # type: ignore
            menu.console.print("[bold purple]Gerando dados simulados...[/bold purple]")
            dados_simulados = simulador.generate_data()
            data_manager.save_data(dados_simulados)
            dados_consumo = dados_simulados
            menu.console.print(
                "[bold green]✅ Dados simulados gerados com sucesso![/bold green]"
            )
        else:
            menu.console.print(
                "[bold red]Sistema encerrado. Execute novamente quando tiver dados disponíveis.[/bold red]"
            )
            sys.exit()

    fila = fila_pilha.FilaConsumo(dados_consumo)
    pilha = fila_pilha.PilhaConsumo(dados_consumo)

    menu_actions = {
        1: lambda: menu_logic.view_data_queue(fila),
        2: lambda: menu_logic.view_data_stack(pilha),
        3: lambda: menu_logic.search_fuzzy(
            dados_consumo,
            max_dist=config.config.fuzzy_distance,  # type: ignore
        ),
        4: lambda: menu_logic.search_sequential(dados_consumo),
        5: lambda: menu_logic.search_binary(dados_consumo),
        6: lambda: menu_logic.sort_merge(dados_consumo),
        7: lambda: menu_logic.sort_quick(dados_consumo),
        8: menu_logic.regenerate_data,
        9: lambda: menu_logic.system_settings(config),
        10: menu_logic.exit_system,
    }

    menu.clear_console()

    while True:
        menu.show_main_menu(MENU_CONFIG)
        opcao_input_str = "[bold green]>[/bold green] Digite o número da sua opção [bold magenta][1-9][/bold magenta]"
        opcao = menu.ask_input_int("\n" + opcao_input_str)
        valid_options = menu.get_valid_menu_options(MENU_CONFIG)

        while opcao not in valid_options:
            menu.show_message("❌ Opção inválida. Tente novamente.", "bold red")
            opcao = menu.ask_input_int(opcao_input_str)

        if opcao != menu.get_valid_menu_options(MENU_CONFIG)[-1]:
            menu.clear_console()

        action = menu_actions.get(opcao)  # type: ignore
        if action:
            if opcao == 7:
                dados_consumo = action()
                fila = fila_pilha.FilaConsumo(dados_consumo)
                pilha = fila_pilha.PilhaConsumo(dados_consumo)
            elif opcao == menu.get_valid_menu_options(MENU_CONFIG)[-1]:
                action()
                break
            else:
                action()
        else:
            menu.show_message("❌ Opção não implementada.", "bold red")

        if opcao != 9:
            menu.console.print(
                "[cyan]\nPressione [bold]Enter[/bold] para voltar ao menu...[/cyan]"
            )
            menu.ask_input("")
            menu.clear_console()


if __name__ == "__main__":
    menu.clear_console()
    try:
        main()
    except KeyboardInterrupt:
        menu.show_message("\n👋 Saindo do sistema. Até logo!", "bold magenta")
