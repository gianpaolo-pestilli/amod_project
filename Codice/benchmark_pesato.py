import time
from vertex_cover_PLI import *
from algoritmi_pesato import *


# Helper per calcolare il peso totale della cover
def get_weight(C, G):
    # Somma il peso di ogni nodo nella cover. Se 'peso' manca, assume 1 di default.
    return sum(G.nodes[n].get('peso', 1) for n in C)


def benchmark_pesato(G, PLI_path, PL_path):
    list_total = []

    # --- Algoritmo 0 (PLI Pesato) ---
    t_0 = time.time()
    # Passiamo is_pesato=True per abilitare i pesi nel modello AMPL
    C_0, status_0 = vertex_cover_0(G, PLI_path, "gurobi", is_pesato=True)
    t_1 = time.time()
    # Calcoliamo il peso invece della lunghezza
    weight_0 = get_weight(C_0, G)
    list_total.append([weight_0, t_1 - t_0, (status_0 == 1), (status_0 == 2)])

    # --- Algoritmo 1 ---
    t_0 = time.time()
    C_1 = vertex_cover_pesato_1(G)
    t_1 = time.time()
    list_total.append([get_weight(C_1, G), t_1 - t_0, False, False])

    # --- Algoritmo 2 ---
    t_0 = time.time()
    C_2 = vertex_cover_pesato_2(G)
    t_1 = time.time()
    list_total.append([get_weight(C_2, G), t_1 - t_0, False, False])

    # --- Algoritmo 3 ---
    t_0 = time.time()
    C_3 = vertex_cover_pesato_3(G)
    t_1 = time.time()
    list_total.append([get_weight(C_3, G), t_1 - t_0, False, False])

    # --- Algoritmo 4 (DRD semplice) ---
    t_0 = time.time()
    # Uso la funzione pesata corretta
    C_4, status_4 = vertex_cover_pesato_4(G, PL_path, "gurobi")
    t_1 = time.time()
    list_total.append([get_weight(C_4, G), t_1 - t_0, (status_4 == 1), (status_4 == 2)])

    # --- Algoritmo 4 (Cutting Plane) ---
    t_0 = time.time()
    # Uso la funzione pesata corretta
    C_4b, status_4b = vertex_cover_pesato_4_OCI_cutting_plane(G)
    t_1 = time.time()
    list_total.append([get_weight(C_4b, G), t_1 - t_0, (status_4b == 1), (status_4b == 2)])

    # --- Algoritmo 5 (Duale) ---
    t_0 = time.time()
    C_5 = vertex_cover_pesato_duale_5(G)
    t_1 = time.time()
    list_total.append([get_weight(C_5, G), t_1 - t_0, False, False])

    return list_total


def run_benchmark_pesato_on_list(graphs_list, PLI_path, PL_path):
    num_algos = 7
    tot_times = [0.0] * num_algos
    tot_ratios = [0.0] * num_algos
    has_timeout = [False] * num_algos
    has_problems = [False] * num_algos

    valid_instances = 0

    for G in graphs_list:
        # Processiamo solo se il grafo non è vuoto
        if G.number_of_edges() != 0:
            results = benchmark_pesato(G, PLI_path, PL_path)

            # Recuperiamo i dati del PLI (Algoritmo 0)
            pli_weight = results[0][0]
            pli_problems = results[0][3]

            # Processiamo l'istanza solo se il PLI NON ha avuto problemi
            if not pli_problems:
                valid_instances += 1

                # Ottimo di riferimento (pesato)
                opt_weight = pli_weight if pli_weight > 0 else 1

                for i in range(num_algos):
                    weight, time_exec, timeout, problems = results[i]

                    tot_times[i] += time_exec

                    # Flag persistenti
                    has_timeout[i] = has_timeout[i] or timeout
                    has_problems[i] = has_problems[i] or problems

                    # Accumulo rapporto (Peso Algoritmo / Peso PLI)
                    tot_ratios[i] += (weight / opt_weight)

    # Calcolo medie finali
    summary = []
    if valid_instances > 0:
        for i in range(num_algos):
            avg_ratio = tot_ratios[i] / valid_instances
            avg_time = tot_times[i] / valid_instances
            summary.append([avg_ratio, avg_time, has_timeout[i], has_problems[i]])

    return summary

