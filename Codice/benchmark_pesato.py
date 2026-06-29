from vertex_cover_PLI import *
from algoritmi_pesato import *
import os
import ast
import networkx as nx
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Helper per calcolare il peso totale della cover
def get_weight(C, G):
    # Somma il peso di ogni nodo nella cover. Se 'peso' manca, assume 1 di default.
    return sum(G.nodes[n].get('peso', 1) for n in C)


def benchmark_pesato(G, PLI_path, PL_path):
    list_total = []

    # --- Algoritmo 0 (PLI Pesato) ---
    t_0 = time.time()
    C_0, status_0 = vertex_cover_0(G, PLI_path, "gurobi", is_pesato=True)
    t_1 = time.time()
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
    C_4, status_4 = vertex_cover_pesato_4(G, PL_path, "gurobi")
    t_1 = time.time()
    list_total.append([get_weight(C_4, G), t_1 - t_0, (status_4 == 1), (status_4 == 2)])

    # --- Algoritmo 4 (Cutting Plane) ---
    t_0 = time.time()
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
        if G.number_of_edges() != 0:
            results = benchmark_pesato(G, PLI_path, PL_path)

            # Recuperiamo i dati del PLI (Algoritmo 0)
            pli_weight = results[0][0]
            pli_problems = results[0][3]

            # Processiamo l'istanza solo se il PLI NON ha avuto problemi
            if not pli_problems:
                valid_instances += 1

                # Ottimo di riferimento
                opt_weight = pli_weight if pli_weight > 0 else 1

                for i in range(num_algos):
                    weight, time_exec, timeout, problems = results[i]

                    tot_times[i] += time_exec

                    has_timeout[i] = has_timeout[i] or timeout
                    has_problems[i] = has_problems[i] or problems
                    tot_ratios[i] += (weight / opt_weight)

    # Calcolo medie finali
    summary = []
    if valid_instances > 0:
        for i in range(num_algos):
            avg_ratio = tot_ratios[i] / valid_instances
            avg_time = tot_times[i] / valid_instances
            summary.append([avg_ratio, avg_time, has_timeout[i], has_problems[i]])

    return summary


def crea_grafo_da_riga(row):
    n = int(row['nodi_effettivi'])
    edges = ast.literal_eval(row['lista_archi'])
    pesi_dict = ast.literal_eval(row['pesi_nodi'])

    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)

    # Assegnazione pesi ai nodi usando il dizionario estratto
    nx.set_node_attributes(G, pesi_dict, 'peso')
    return G


def salva_benchmark_in_pdf_pesato(summary, nome_classe, pdf_obj):
    algo_names = ["PLI", "Algo_1", "Algo_2", "Algo_3", "DRD", "Cut&DRD", "Duale"]

    ratios = [row[0] for row in summary]
    times = [row[1] for row in summary]

    # Colori: Successo=Verde, Timeout=Rosso, Crash=Blu
    colors = ['blue' if row[3] else ('red' if row[2] else 'green') for row in summary]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"Benchmark PESATO: {nome_classe}", fontsize=16)

    ax1.bar(algo_names, ratios, color=colors, edgecolor='black', alpha=0.7)
    ax1.set_title("Rapporto di Approssimazione Medio")
    ax1.set_ylabel("Ratio (Alg / PLI)")
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    ax2.bar(algo_names, times, color=colors, edgecolor='black', alpha=0.7)
    ax2.set_title("Tempo medio di esecuzione (sec)")
    ax2.set_ylabel("Secondi")
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    # Legenda
    legend_handles = [
        mpatches.Patch(color='green', label='Successo'),
        mpatches.Patch(color='red', label='Timeout'),
        mpatches.Patch(color='blue', label='Crash')
    ]
    fig.legend(handles=legend_handles, loc='upper right')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    pdf_obj.savefig(fig)
    plt.close(fig)


def overall_pesato(PLI_path, PL_path, CSV_path):
    print("Avvio Benchmark PESATO: Salvataggio blindato a batch separati.")

    reader = pd.read_csv(CSV_path, chunksize=15)

    for i, chunk in enumerate(reader):
        batch_id = i + 1
        nome_file_batch = f"Report_Batch_Pesato_{batch_id:02d}.pdf"

        if os.path.exists(nome_file_batch):
            print(f"Batch {batch_id} già completato, salto...")
            continue

        chunk_5 = chunk.iloc[:5]
        row = chunk_5.iloc[0]
        nome_classe = f"N:{row['n_target']} | D:{row['d_target']} | B:{row['b_val']} | Sp:{row['spearman']}"

        print(f"Processando {nome_classe} (Batch {batch_id})...")

        try:
            list_graphs = [crea_grafo_da_riga(r) for _, r in chunk_5.iterrows()]
            summary = run_benchmark_pesato_on_list(list_graphs, PLI_path, PL_path)
            with PdfPages(nome_file_batch) as pdf:
                salva_benchmark_in_pdf_pesato(summary, nome_classe, pdf)

            print(f"  -> Salvato: {nome_file_batch}")

        except Exception as e:
            print(f"\n!!! Errore critico nel batch {batch_id}: {e} !!!")
            continue