# In questo file ci sono gli algoritmi per vertici non pesati
import time

from amplpy import AMPL
import gurobipy as gp
from gurobipy import GRB


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

    if solver.lower() == 'gurobi':
        ampl.setOption("gurobi_options", "timelimit=10 numericfocus=1")

    ampl.read(model_path)
    ampl.set["V"] = list(G.nodes())
    ampl.set["E"] = list(G.edges())

    ampl.param["c"] = {n: 1 for n in G.nodes()}
    ampl.solve()
    solve_result = ampl.getValue('solve_result')

    if solve_result == 'limit':
        status = 1
    elif solve_result in ['failure', 'infeasible']:
        status = 2
    else:
        status = 0
    C = set()

    if status != 2:
        x_values = ampl.get_variable("x").get_values().to_dict()
        if x_values:
            C = {nodo for nodo, valore in x_values.items() if valore >= 0.5}

    if not C:
        C = set(G.nodes())

    return C, status


def vertex_cover_non_pesato_4_OCI_cutting_plane(G):
    triangoli_set = set()
    for u, v in G.edges():
        vicini_comuni = set(G.neighbors(u)).intersection(G.neighbors(v))
        for w in vicini_comuni:
            triangoli_set.add(tuple(sorted((u, v, w))))
    triangoli = list(triangoli_set)

    model = gp.Model("Cutting plane")
    model.Params.OutputFlag = 0

    # Limiti RAM
    model.Params.Threads = 1
    model.Params.NodefileStart = 1.0

    x = model.addVars(G.nodes(), vtype=GRB.CONTINUOUS, lb=0.0, ub=1.0, name="x")
    model.setObjective(gp.quicksum(x[i] for i in G.nodes()), GRB.MINIMIZE)

    for u, v in G.edges():
        model.addConstr(x[u] + x[v] >= 1)

    best_C = set()
    status = 0
    start_time = time.time()

    while True:
        tempo_rimasto = 10.0 - (time.time() - start_time)
        if tempo_rimasto <= 0:
            status = 1  # Timeout
            break

        model.Params.TimeLimit = tempo_rimasto
        model.optimize()

        if model.Status == GRB.TIME_LIMIT:
            status = 1
            break
        elif model.Status != GRB.OPTIMAL:
            status = 2  # Errore/Infeasible
            break

        x_vals = model.getAttr('X', x)
        best_C = {i for i in G.nodes() if x_vals[i] >= 0.5}

        tagli_da_aggiungere = []
        for u, v, w in triangoli:
            if x_vals[u] + x_vals[v] + x_vals[w] < 1.999:
                tagli_da_aggiungere.append((u, v, w))

        if len(tagli_da_aggiungere) == 0:
            break

        for u, v, w in tagli_da_aggiungere:
            model.addConstr(x[u] + x[v] + x[w] >= 2)

    # Fallback estremo se non ha trovato nulla al primo giro
    if not best_C:
        best_C = set(G.nodes())

    return best_C, status


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