from ui import menu, menu_logic
from utils import data_manager, simulador
import sys

MENU_CONFIG = {
    "panel_title": "[bold magenta]🏥 Gerenciador de Insumos de Diagnóstico[/bold magenta]",
    "panel_border_style": "bold cyan",
    "groups": [
        {
            "title": "🔧 GERENCIAMENTO",
            "color": "cyan",
            "options": [
                {
                    "number": 7,
                    "description": "Regenerar Dados Simulados",
                },
                {
                    "number": 8,
                    "description": "Configurações do Sistema",
                },
            ],
        },
        {
            "title": "🚪 SISTEMA",
            "color": "red",
            "options": [
                {
                    "number": 9,
                    "description": "Sair",
                },
            ],
        },
    ],
}


def main():
    """Função principal que executa o loop da aplicação."""
    dados_consumo = data_manager.load_data()

    if not dados_consumo:
        menu.console.print(
            "[bold yellow]Atenção:[/bold yellow] O arquivo 'data/consumo.json' está vazio ou não foi encontrado."
        )
        resposta = menu.ask_input(
            "Deseja gerar dados simulados automaticamente?", choices=["s", "n"]
        )

        if resposta.lower() == "s":
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

    menu_actions = {
        7: menu_logic.regenerate_data,
        8: menu_logic.system_settings,
        9: menu_logic.exit_system,
    }

    menu.clear_console()

    while True:
        menu.show_main_menu(MENU_CONFIG)
        opcao_input_str = (
            "[bold green]>[/bold green] Digite o número da sua opção "
            f"[bold magenta]({min(menu.get_valid_menu_options(MENU_CONFIG))}-"
            f"{max(menu.get_valid_menu_options(MENU_CONFIG))})[/bold magenta]: "
        )
        opcao = menu.ask_input_int("\n" + opcao_input_str)
        valid_options = menu.get_valid_menu_options(MENU_CONFIG)

        while opcao not in valid_options:
            menu.show_message("❌ Opção inválida. Tente novamente.", "bold red")
            opcao = menu.ask_input_int(opcao_input_str)

        if opcao != menu.get_valid_menu_options(MENU_CONFIG)[-1]:
            menu.clear_console()

        action = menu_actions.get(opcao)  # type: ignore
        if action:
            if opcao == 9:
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
