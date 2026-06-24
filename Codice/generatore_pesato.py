import networkx as nx
import numpy as np


def genera_singola_istanza_pesata(n, densita_target, variabilita_peso, correlazione_spearman):
    G = nx.erdos_renyi_graph(n, p=densita_target)
    pesi_generati = np.random.randint(1, variabilita_peso + 1, size=n)

    if correlazione_spearman == 0:
        np.random.shuffle(pesi_generati)
        mapping_pesi = {nodo: int(peso) for nodo, peso in zip(G.nodes(), pesi_generati)}

    else:
        nodi_ordinati = sorted(G.nodes(), key=lambda x: G.degree(x))
        pesi_ordinati = sorted(pesi_generati)

        if correlazione_spearman == -1:
            pesi_ordinati = pesi_ordinati[::-1]

        mapping_pesi = {nodo: int(peso) for nodo, peso in zip(nodi_ordinati, pesi_ordinati)}

    nx.set_node_attributes(G, mapping_pesi, 'peso')

    return G