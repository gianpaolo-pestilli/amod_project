import networkx as nx
import numpy as np


def genera_singola_istanza_pesata(n, densita_target, variabilita_peso, correlazione_spearman):
    """
    Genera un singolo grafo pesato con topologia Erdős-Rényi.

    :param n: Numero di nodi
    :param densita_target: Densità del grafo (es. 0.2, 0.5, 0.8)
    :param variabilita_peso: Max peso vertice (es. 10, 1000, 10000)
    :param correlazione_spearman: -1 (Inversa), 0 (Nessuna), 1 (Diretta)
    :return: Oggetto nx.Graph con attributo 'peso' sui nodi
    """
    # 1. Generazione Topologia
    G = nx.erdos_renyi_graph(n, p=densita_target)

    # 2. Generazione Pesi (Distribuzione Uniforme Discreta)
    pesi_generati = np.random.randint(1, variabilita_peso + 1, size=n)

    # 3. Mappatura Pesi-Nodi basata su Spearman
    if correlazione_spearman == 0:
        np.random.shuffle(pesi_generati)
        mapping_pesi = {nodo: int(peso) for nodo, peso in zip(G.nodes(), pesi_generati)}

    else:
        # Ordino i nodi per grado crescente
        nodi_ordinati = sorted(G.nodes(), key=lambda x: G.degree(x))
        # Ordino i pesi per valore crescente
        pesi_ordinati = sorted(pesi_generati)

        if correlazione_spearman == -1:
            # Correlazione inversa: ribalto i pesi (grado alto -> peso basso)
            pesi_ordinati = pesi_ordinati[::-1]

        mapping_pesi = {nodo: int(peso) for nodo, peso in zip(nodi_ordinati, pesi_ordinati)}

    # 4. Assegnazione attributi
    nx.set_node_attributes(G, mapping_pesi, 'peso')

    return G