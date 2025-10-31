def busca_sequencial(lista, chave, valor):
    """Realiza uma busca sequencial em uma lista de dicionários.

    Complexidade: O(n), onde n é o tamanho da lista.
    """
    resultados = []
    valor_busca = str(valor).lower()
    for item in lista:
        campo = str(item.get(chave)).lower()
        if valor_busca in campo:
            resultados.append(item)
    return resultados if resultados else None


def busca_binaria(lista_ordenada, chave, valor):
    """Realiza uma busca binária em uma lista de dicionários.
    A lista DEVE estar pré-ordenada pela 'chave'.

    Complexidade: O(log n), onde n é o tamanho da lista.
    """
    baixo, alto = 0, len(lista_ordenada) - 1
    valor_busca = str(valor).lower()
    resultados = []

    while baixo <= alto:
        meio = (baixo + alto) // 2
        valor_meio_obj = lista_ordenada[meio].get(chave)
        valor_meio = str(valor_meio_obj).lower()

        if valor_busca in valor_meio:
            i = meio
            while i >= 0:
                campo = str(lista_ordenada[i].get(chave)).lower()
                if valor_busca in campo:
                    resultados.append(lista_ordenada[i])
                    i -= 1
                else:
                    break
            i = meio + 1
            while i < len(lista_ordenada):
                campo = str(lista_ordenada[i].get(chave)).lower()
                if valor_busca in campo:
                    resultados.append(lista_ordenada[i])
                    i += 1
                else:
                    break
            return resultados
        elif valor_meio < valor_busca:
            baixo = meio + 1
        else:
            alto = meio - 1
    return None


if __name__ == "__main__":
    dados_teste = [
        {
            "nome_insumo": "Reagente A",
            "quantidade_consumida": 50,
            "validade": "2024-12-31",
        },
        {
            "nome_insumo": "Reagente B",
            "quantidade_consumida": 20,
            "validade": "2023-11-30",
        },
        {
            "nome_insumo": "Reagente C",
            "quantidade_consumida": 75,
            "validade": "2025-01-15",
        },
    ]

    print("Busca Sequencial por 'Reagente B':")
    resultado_seq = busca_sequencial(dados_teste, "nome_insumo", "Reagente B")
    print(resultado_seq if resultado_seq else "Insumo não encontrado.")

    print("\nBusca Binária por 'Reagente C' (lista ordenada):")
    dados_ordenados = sorted(dados_teste, key=lambda x: x["nome_insumo"])
    resultado_bin = busca_binaria(dados_ordenados, "nome_insumo", "Reagente C")
    print(resultado_bin if resultado_bin else "Insumo não encontrado.")
