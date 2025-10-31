def busca_fuzzy_iter(dados, chave, termo, max_dist=2):
    """Retorna itens cujo campo 'chave' é semelhante ao termo (fuzzy search)."""
    resultados = []
    for item in dados:
        # Otimização: Se a diferença de tamanho já é maior que a distância máxima, é impossível a distância de Levenshtein ser <= max_dist.
        if abs(len(item[chave]) - len(termo)) > max_dist:
            continue

        dist = levenshtein_distance_iter(item[chave], termo)
        if dist <= max_dist:
            resultados.append(item)
    return resultados


def levenshtein_distance_iter(s1, s2):
    """
    Calcula a distância de Levenshtein entre duas strings de forma iterativa (bottom-up).
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1].lower() == s2[j - 1].lower() else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # remoção
                dp[i][j - 1] + 1,  # inserção
                dp[i - 1][j - 1] + cost,  # substituição
            )
    return dp[m][n]


def busca_fuzzy_rec(dados, chave, termo, max_dist=2):
    """
    Retorna itens cujo campo 'chave' é semelhante ao termo (fuzzy search) utilizando distância de Levenshtein recursiva.

    Complexidade de tempo: O(N * m * n)
    Onde N é o número de itens em 'dados', m é o comprimento da string no campo 'chave' e n é o comprimento do 'termo'.
    """
    resultados = []
    for item in dados:
        # Otimização: Se a diferença de tamanho já é maior que a distância máxima, é impossível a distância de Levenshtein ser <= max_dist.
        if abs(len(item[chave]) - len(termo)) > max_dist:
            continue

        dist = levenshtein_distance_rec(item[chave], termo)
        if dist <= max_dist:
            resultados.append(item)
    return resultados


def levenshtein_distance_rec(s1, s2):
    """
    Calcula a distância de Levenshtein entre duas strings usando recursão e cache manual.

    Complexidade de tempo: O(m * n)
    Complexidade de tempo sem cache: O(3^(m+n))
    """
    cache = {}

    def rec(i, j):
        if (i, j) in cache:
            return cache[(i, j)]
        if i == 0:
            result = j
        elif j == 0:
            result = i
        else:
            cost = 0 if s1[i - 1].lower() == s2[j - 1].lower() else 1
            result = min(
                rec(i - 1, j) + 1,  # remoção
                rec(i, j - 1) + 1,  # inserção
                rec(i - 1, j - 1) + cost,  # substituição
            )
        cache[(i, j)] = result
        return result

    return rec(len(s1), len(s2))


if __name__ == "__main__":
    s1 = "Augusto"
    s2 = "Augto"
    iter_distance = levenshtein_distance_iter(s1, s2)
    rec_distance = levenshtein_distance_rec(s1, s2)
    print(f"Distância iterativa entre '{s1}' e '{s2}': {iter_distance}")
    print(f"Distância recursiva entre '{s1}' e '{s2}': {rec_distance}")
