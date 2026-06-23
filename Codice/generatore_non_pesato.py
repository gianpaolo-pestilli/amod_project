import networkx as nx
import numpy as np


def _applica_configuration_model(n, gradi_float):
    """
    Converte un array di numeri float in un grafo valido.
    """
    # 1. Arrotonda i float a interi
    gradi_int = np.round(gradi_float).astype(int)

    # 2. Taglia eventuali valori sballati (nessun nodo < 0 o > n-1 archi)
    gradi_int = np.clip(gradi_int, 0, n - 1)

    # 3. La somma dei gradi deve essere pari (teorema strette di mano)
    if np.sum(gradi_int) % 2 != 0:
        idx = np.random.randint(0, n)
        gradi_int[idx] += 1 if gradi_int[idx] < n - 1 else -1

    # 4. Genera il grafo e rimuove i self-loop (auto-anelli)
    G_multi = nx.configuration_model(gradi_int)
    G = nx.Graph(G_multi)
    G.remove_edges_from(nx.selfloop_edges(G))
    return G


def genera_singola_istanza(n, densita_target, classe_eterogeneita):
    """
    Genera un singolo grafo in base ai parametri richiesti.

    :param n: Numero di nodi
    :param densita_target: Densità attesa (es. 0.2, 0.5)
    :param classe_eterogeneita: 0 (Regolare), 1 (Gaussiana), 2 (Lognormale)
    :return: Oggetto nx.Graph
    """
    k_medio_atteso = densita_target * (n - 1)

    # CLASSE 0: Grafo Regolare (Eterogeneità = 1)
    if classe_eterogeneita == 0:
        k = int(np.round(k_medio_atteso))
        if (n * k) % 2 != 0:
            k += 1
        return nx.random_regular_graph(k, n)

    # CLASSE 1: Campana Stretta (Eterogeneità 1.2 - 1.6)
    elif classe_eterogeneita == 1:
        std_dev = k_medio_atteso * 0.15
        while True:
            gradi_float = np.random.normal(loc=k_medio_atteso, scale=std_dev, size=n)
            H = np.max(gradi_float) / np.mean(gradi_float)
            if 1.2 <= H <= 1.6:
                return _applica_configuration_model(n, gradi_float)

    # CLASSE 2: Presenza di Hub (Eterogeneità > 2)
    elif classe_eterogeneita == 2:
        while True:
            sigma = 1.0
            mu = np.log(k_medio_atteso) - (sigma ** 2 / 2)
            gradi_float = np.random.lognormal(mean=mu, sigma=sigma, size=n)
            H = np.max(gradi_float) / np.mean(gradi_float)
            if H > 2.0:
                return _applica_configuration_model(n, gradi_float)

    else:
        raise ValueError(f"Classe {classe_eterogeneita} non valida. Usa 0, 1 o 2.")