# In questo file ci sono gli algoritmi per vertici pesati

from amplpy import AMPL

def vertex_cover_pesato_1(G):
    C = set()
    archi_coperti = set()
    W = [n for p, n in sorted([(G.nodes[n]['peso'], n) for n in G.nodes()])]

    for v in W:
        C.add(v)

        for arco in G.edges(v):
            archi_coperti.add(tuple(sorted(arco)))

        if len(archi_coperti) == G.number_of_edges():
            return C

    return C


def vertex_cover_pesato_2(G):
    C = set()
    archi_coperti = set()

    # Ordino per rapporto peso/grado
    coppie = [(G.nodes[n]['peso'] / G.degree(n) if G.degree(n) > 0 else float('inf'), n) for n in G.nodes()]
    coppie.sort()
    W = [n for rapporto, n in coppie]

    for v in W:
        C.add(v)

        for arco in G.edges(v):
            archi_coperti.add(tuple(sorted(arco)))

        if len(archi_coperti) == G.number_of_edges():
            return C

    return C


def vertex_cover_pesato_3(G):
    C = set()
    archi_coperti = set()
    lista_archi = []
    for u, v in G.edges():
        peso_totale = G.nodes[u]['peso'] + G.nodes[v]['peso']
        lista_archi.append((peso_totale, u, v))
    lista_archi.sort()

    for peso, u, v in lista_archi:
        arco = tuple(sorted((u, v))) #lo uso per avere coppie ordinate (1,2) = (2,1)
        if arco not in archi_coperti:
            C.add(u)
            C.add(v)

            for a in G.edges(u):
                archi_coperti.add(tuple(sorted(a)))
            for a in G.edges(v):
                archi_coperti.add(tuple(sorted(a)))

    return C


def vertex_cover_pesato_4(G, model_path, solver):
    ampl = AMPL()
    ampl.setOption("solver", solver)
    ampl.read(model_path)
    ampl.set["V"] = list(G.nodes())
    ampl.set["E"] = list(G.edges())

    pesi = {}
    for n in G.nodes():
        pesi[n] = G.nodes[n]['peso']
    ampl.param["c"] = pesi

    ampl.solve()

    x_values = ampl.get_variable("x").get_values().to_dict()
    C = {nodo for nodo, valore in x_values.items() if valore >= 0.5}
    return C

def vertex_cover_pesato_duale_5(G):

    x = {n: 0 for n in G.nodes()}
    y = {tuple(sorted(e)): 0 for e in G.edges()}
    I = {tuple(sorted(e)) for e in G.edges()}

    while I:
        e = list(I)[0]
        (u, v) = e

        sum_y_u = sum(y[tuple(sorted(edge))] for edge in G.edges(u))
        sum_y_v = sum(y[tuple(sorted(edge))] for edge in G.edges(v))

        increment_u = G.nodes[u]['peso'] - sum_y_u
        increment_v = G.nodes[v]['peso'] - sum_y_v

        if increment_u <= increment_v:
            y[e] = increment_u
            x[u] = 1
            I -= {tuple(sorted(edge)) for edge in G.edges(u)}

        else:
            y[e] = increment_v
            x[v] = 1
            I -= {tuple(sorted(edge)) for edge in G.edges(v)}
            
    # Ritorno i nodi marcati (in cover)
    return {n for n, valore in x.items() if valore == 1}