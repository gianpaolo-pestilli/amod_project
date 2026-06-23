# In questo file ci sono gli algoritmi per vertici non pesati

from amplpy import AMPL
import gurobipy as gp
from gurobipy import GRB
import networkx as nx

def vertex_cover_non_pesato_1(G):
    C = set()
    archi_da_coprire = G.number_of_edges()
    for v in G.nodes():
        C.add(v)
        for u in G.neighbors(v):
            if u not in C:
                archi_da_coprire -= 1

        # Se ho coperto tutti gli archi
        if archi_da_coprire == 0:
            return C

    return C

def vertex_cover_non_pesato_2(G):
    C = set()
    archi_da_coprire = G.number_of_edges()

    # Ordino i vertici per grado decrescente
    W = sorted(G.nodes(), key=G.degree, reverse=True)

    for v in W:
        C.add(v)
        for u in G.neighbors(v):
            if u not in C:
                archi_da_coprire -= 1
        # Coperti tutti gli archi
        if archi_da_coprire == 0:
            return C

    return C


def vertex_cover_non_pesato_3(G):
    C = set()
    for u, v in G.edges():
        # Se non ho vertici nel cover => l'arco è scoperto
        if u not in C and v not in C:
            # Prendo entrambi i vertici e li metto nella cover
            C.add(u)
            C.add(v)
            # Non necessito di costruire la rete residua:
            # L'inserimento dei nodi nell'insieme C equivale a rimuovere le stelle uscenti
    return C


def vertex_cover_non_pesato_4_simple_DRD(G, model_path, solver):
    ampl = AMPL()
    ampl.setOption("solver", solver)
    ampl.read(model_path)
    ampl.set["V"] = list(G.nodes())
    ampl.set["E"] = list(G.edges())

    # Imposto i pesi a 1
    ampl.param["c"] = {n: 1 for n in G.nodes()}
    ampl.set["TRIANGOLI"] = [] # non ho odd inequalities
    ampl.solve()
    x_values = ampl.get_variable("x").get_values().to_dict()
    # Uso doubling and rounding down
    C = {nodo for nodo, valore in x_values.items() if valore >= 0.5}
    return C


def vertex_cover_non_pesato_4_OCE_priori_ampl(G, model_path, solver):
    # Trovo i triangoli
    triangoli = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]
    ampl = AMPL()
    ampl.setOption("solver", solver)
    ampl.read(model_path)

    # Passo i dati
    ampl.set["V"] = list(G.nodes())
    ampl.set["E"] = list(G.edges())
    ampl.param["c"] = {n: 1 for n in G.nodes()}
    # Do i vincoli sui triangoli ad AMPL
    ampl.set["TRIANGOLI"] = triangoli
    # Invoco la risoluzione
    ampl.solve()
    # Classico doubling and rounding down
    x_values = ampl.get_variable("x").get_values().to_dict()
    C = {nodo for nodo, valore in x_values.items() if valore >= 0.5}

    return C




def vertex_cover_non_pesato_4_OCE_cutting_plane(G):
    # Prendo tutti i triangoli
    triangoli = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]

    model = gp.Model("Cutting plane")
    model.Params.OutputFlag = 0
    x = model.addVars(G.nodes(), vtype=GRB.CONTINUOUS, lb=0.0, ub=1.0, name="x")

    model.setObjective(gp.quicksum(x[i] for i in G.nodes()), GRB.MINIMIZE)

    for u, v in G.edges():
        model.addConstr(x[u] + x[v] >= 1)

    while True:
        model.optimize()
        x_vals = model.getAttr('X', x)
        tagli_da_aggiungere = []
        for u, v, w in triangoli:
            # Considero solo i triangoli violati
            if x_vals[u] + x_vals[v] + x_vals[w] < 1.999:
                tagli_da_aggiungere.append((u, v, w))

        if len(tagli_da_aggiungere) == 0:
            break

        # Aggiungo il blocco di vincoli strettamente necessari
        for u, v, w in tagli_da_aggiungere:
            model.addConstr(x[u] + x[v] + x[w] >= 2)
    C = {i for i in G.nodes() if x[i].X >= 0.5}
    return C


def vertex_cover_non_pesato_duale_5(G):
    x = {n: 0 for n in G.nodes()}
    y = {tuple(sorted(e)): 0 for e in G.edges()}
    I = {tuple(sorted(e)) for e in G.edges()}

    while I:
        e = next(iter(I))
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

        else:
            y[e] = increment_u

            if G.degree(u) <= G.degree(v):
                x[v] = 1
                I -= {tuple(sorted(edge)) for edge in G.edges(v)}
            else:
                x[u] = 1
                I -= {tuple(sorted(edge)) for edge in G.edges(u)}
    return {n for n, valore in x.items() if valore == 1}