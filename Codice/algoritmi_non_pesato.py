# In questo file ci sono gli algoritmi per vertici non pesati

from amplpy import AMPL

def vertex_cover_non_pesato_1(G):
    C = set()
    archi_coperti = set() # Per cancellare gli archi senza fisicamente rimuoverli dal grafo

    for v in G.nodes():
        # Metto il nodo in cover
        C.add(v)

        # "Cancello" la stella uscente
        for arco in G.edges(v):
            archi_coperti.add(tuple(sorted(arco)))

        # Se ho coperto tutti gli archi esco
        if len(archi_coperti) == G.number_of_edges():
            return C

    return C


def vertex_cover_non_pesato_2(G):
    C = set()
    archi_coperti = set()

    # Ordino i vertici per grado decrescente
    W = sorted(G.nodes(), key=G.degree, reverse=True)

    for v in W:
        C.add(v)

        for arco in G.edges(v):
            archi_coperti.add(tuple(sorted(arco)))

        if len(archi_coperti) == G.number_of_edges():
            return C

    return C


def vertex_cover_non_pesato_3(G):
    C = set()
    I = {tuple(sorted(e)) for e in G.edges()} # Copio l'insieme degli archi per cancellarli

    while I:
        (u, v) = I.pop()

        # Metto in cover
        C.add(u)
        C.add(v)

        # Creo l'insieme unione delle stelle uscenti
        J = {tuple(sorted(e)) for e in list(G.edges(u)) + list(G.edges(v))}

        # Rimuovo le stelle uscenti dall'insieme degli archi
        I -= J

    return C


def vertex_cover_non_pesato_4(G, model_path, solver):
    ampl = AMPL()
    ampl.setOption("solver", solver)
    ampl.read(model_path)
    ampl.set["V"] = list(G.nodes())
    ampl.set["E"] = list(G.edges())

    # Imposto i pesi a 1
    ampl.param["c"] = {n: 1 for n in G.nodes()}
    ampl.solve()
    x_values = ampl.get_variable("x").get_values().to_dict()
    # Uso doubling and rounding down
    C = {nodo for nodo, valore in x_values.items() if valore >= 0.5}
    return C


def vertex_cover_non_pesato_duale_5(G):
    x = {n: 0 for n in G.nodes()}
    y = {tuple(sorted(e)): 0 for e in G.edges()}

    # Insieme di tutti gli archi
    I = {tuple(sorted(e)) for e in G.edges()}

    while I:
        # Prendo un arco
        e = list(I)[0]
        (u, v) = e

        sum_y_u = sum(y[tuple(sorted(edge))] for edge in G.edges(u))
        sum_y_v = sum(y[tuple(sorted(edge))] for edge in G.edges(v))

        increment_u = 1 - sum_y_u
        increment_v = 1 - sum_y_v

        if increment_u < increment_v:
            y[e] = 0
            x[u] = 1
            I -= {tuple(sorted(edge)) for edge in G.edges(u)}

        elif increment_u > increment_v:
            y[e] = 0
            x[v] = 1
            I -= {tuple(sorted(edge)) for edge in G.edges(v)}

        else:  # sono uguali
            y[e] = increment_u

            if G.degree(u) <= G.degree(v):
                x[v] = 1
                I -= {tuple(sorted(edge)) for edge in G.edges(v)}
            else:
                x[u] = 1
                I -= {tuple(sorted(edge)) for edge in G.edges(u)}

    # Ritorno i nodi marcati (in cover)
    return {n for n, valore in x.items() if valore == 1}