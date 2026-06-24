# In questo file ci sono gli algoritmi per vertici pesati

from amplpy import AMPL
import gurobipy as gp
from gurobipy import GRB
import networkx as nx

def vertex_cover_pesato_1(G):
    num_edges = G.number_of_edges()
    if num_edges == 0:
        return set()

    C = set()
    n_archi_coperti = 0
    W = sorted(G.nodes(), key=lambda x: (G.nodes[x]['peso'], x))
    for v in W:
        C.add(v)
        for u in G.neighbors(v):
            if u not in C:
                n_archi_coperti += 1
        if n_archi_coperti == num_edges:
            break

    return C


def vertex_cover_pesato_2(G):
    num_edges = G.number_of_edges()
    if num_edges == 0:
        return set()
    C = set()
    n_archi_coperti = 0
    W = sorted(
        G.nodes(),
        key=lambda n: (G.nodes[n]['peso'] / G.degree(n) if G.degree(n) > 0 else float('inf'), n)
    )

    for v in W:
        C.add(v)

        for u in G.neighbors(v):
            if u not in C:
                n_archi_coperti += 1

        if n_archi_coperti == num_edges:
            break

    return C


def vertex_cover_pesato_3(G):
    C = set()
    lista_archi = []
    for u, v in G.edges():
        peso_totale = G.nodes[u]['peso'] + G.nodes[v]['peso']
        lista_archi.append((peso_totale, u, v))
    lista_archi.sort()

    for peso, u, v in lista_archi:
        if u not in C and v not in C:
            C.add(u)
            C.add(v)
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
    ampl.set["TRIANGOLI"] = []
    ampl.solve()

    x_values = ampl.get_variable("x").get_values().to_dict()
    C = {nodo for nodo, valore in x_values.items() if valore >= 0.5}
    return C

def vertex_cover_pesato_4_OCE_priori_ampl(G, model_path, solver):
    ampl = AMPL()
    ampl.setOption("solver", solver)
    ampl.read(model_path)

    ampl.set["V"] = list(G.nodes())
    ampl.set["E"] = list(G.edges())
    ampl.param["c"] = {n: G.nodes[n]['peso'] for n in G.nodes()}
    triangoli_set = set()
    for u, v in G.edges():
        vicini_comuni = set(G.neighbors(u)).intersection(G.neighbors(v))
        for w in vicini_comuni:
            triangoli_set.add(tuple(sorted((u, v, w))))
    triangoli = list(triangoli_set)
    ampl.set["TRIANGOLI"] = triangoli

    ampl.solve()

    x_values = ampl.get_variable("x").get_values().to_dict()
    C = {nodo for nodo, valore in x_values.items() if valore >= 0.5}
    return C


def vertex_cover_pesato_4_OCE_cutting_plane(G):

    triangoli_set = set()
    for u, v in G.edges():
        vicini_comuni = set(G.neighbors(u)).intersection(G.neighbors(v))
        for w in vicini_comuni:
            triangoli_set.add(tuple(sorted((u, v, w))))
    triangoli = list(triangoli_set)

    model = gp.Model("Weighted_Cutting_Plane_Dinamico")
    model.Params.OutputFlag = 0

    x = model.addVars(G.nodes(), vtype=GRB.CONTINUOUS, lb=0.0, ub=1.0, name="x")

    model.setObjective(
        gp.quicksum(G.nodes[i]['peso'] * x[i] for i in G.nodes()),
        GRB.MINIMIZE
    )

    for u, v in G.edges():
        model.addConstr(x[u] + x[v] >= 1)

    while True:
        model.optimize()
        x_vals = model.getAttr('X', x)

        tagli_da_aggiungere = []

        for u, v, w in triangoli:
            if x_vals[u] + x_vals[v] + x_vals[w] < 1.999:
                tagli_da_aggiungere.append((u, v, w))

        if not tagli_da_aggiungere:
            break

        for u, v, w in tagli_da_aggiungere:
            model.addConstr(x[u] + x[v] + x[w] >= 2)

    C = {i for i in G.nodes() if x[i].X >= 0.5}
    return C


def vertex_cover_pesato_duale_5(G):
    x = {n: 0 for n in G.nodes()}
    y = {tuple(sorted(e)): 0 for e in G.edges()}
    I = {tuple(sorted(e)) for e in G.edges()}

    while I:
        e = next(iter(I))
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
    return {n for n, valore in x.items() if valore == 1}