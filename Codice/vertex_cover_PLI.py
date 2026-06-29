from amplpy import AMPL


def vertex_cover_0(G, model_path, solver, is_pesato=False):
    ampl = AMPL()
    ampl.setOption("solver", solver)

    if solver.lower() == 'gurobi':
        ampl.setOption("gurobi_options", "timelimit=8")

    ampl.read(model_path)
    ampl.set["V"] = list(G.nodes())
    ampl.set["E"] = list(G.edges())

    if is_pesato:
        ampl.param["c"] = {n: G.nodes[n]['peso'] for n in G.nodes()}
    else:
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
            C = {nodo for nodo, valore in x_values.items() if valore >= 0.999}

    if not C:
        C = set(G.nodes())

    return C, status