import networkx as nx
import numpy as np


def applica_configuration_model(n, gradi_float):
    gradi_int = np.round(gradi_float).astype(int)
    gradi_int = np.clip(gradi_int, 0, n - 1)
    if np.sum(gradi_int) % 2 != 0:
        idx = np.random.randint(0, n)
        gradi_int[idx] += 1 if gradi_int[idx] < n - 1 else -1
    G_multi = nx.configuration_model(gradi_int)
    G = nx.Graph(G_multi)
    G.remove_edges_from(nx.selfloop_edges(G))
    return G


def genera_singola_istanza(n, densita_target, classe_eterogeneita):
    k_medio_atteso = densita_target * (n - 1)

    if classe_eterogeneita == 0:
        k = int(np.round(k_medio_atteso))
        if (n * k) % 2 != 0:
            k += 1
        return nx.random_regular_graph(k, n)
    elif classe_eterogeneita == 1:
        std_dev = k_medio_atteso * 0.14
        while True:
            gradi_float = np.random.normal(loc=k_medio_atteso, scale=std_dev, size=n)
            H = np.max(gradi_float) / np.mean(gradi_float)
            if 1.2 <= H <= 1.6:
                return applica_configuration_model(n, gradi_float)
    elif classe_eterogeneita == 2:
        while True:
            sigma = 1.0
            mu = np.log(k_medio_atteso) - (sigma ** 2 / 2)
            gradi_float = np.random.lognormal(mean=mu, sigma=sigma, size=n)
            H = np.max(gradi_float) / np.mean(gradi_float)
            if H > 2.0:
                return applica_configuration_model(n, gradi_float)
    else:
        raise ValueError(f"Classe {classe_eterogeneita} non valida. Usa 0, 1 o 2.")