from vertex_cover_PLI import *
from algoritmi_non_pesato import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import ast
import networkx as nx

def benchmark_np(G, PLI_path, PL_path):
    list_total = []
    # Algoritmo 0 (uso del solver di PLI)
    t_0 = time.time()
    algo_0 = vertex_cover_0(G,PLI_path,"gurobi")
    t_1 = time.time()
    delta_time = t_1 - t_0
    cover_opt_val = len(algo_0[0])
    status = algo_0[1]
    timeout = False
    problems = False

    if status == 1:
        timeout = True

    if status == 2:
        problems = True

    algo_list = [cover_opt_val,delta_time, timeout, problems]
    list_total.append(algo_list)

    # Algoritmo 1
    t_0 = time.time()
    algo_1 = vertex_cover_non_pesato_1(G)
    t_1 = time.time()
    delta_time = t_1 - t_0
    cover_opt_val = len(algo_1)
    timeout = False
    problems = False
    algo_list = [cover_opt_val,delta_time, timeout, problems]
    list_total.append(algo_list)

    # Algoritmo 2
    t_0 = time.time()
    algo_2 = vertex_cover_non_pesato_2(G)
    t_1 = time.time()
    delta_time = t_1 - t_0
    cover_opt_val = len(algo_2)
    timeout = False
    problems = False
    algo_list = [cover_opt_val,delta_time, timeout, problems]
    list_total.append(algo_list)

    # Algoritmo 3
    t_0 = time.time()
    algo_3 = vertex_cover_non_pesato_3(G)
    t_1 = time.time()
    delta_time = t_1 - t_0
    cover_opt_val = len(algo_3)
    timeout = False
    problems = False
    algo_list = [cover_opt_val,delta_time, timeout, problems]
    list_total.append(algo_list)

    # Algoritmo 4 con DRD semplice
    t_0 = time.time()
    algo_4 = vertex_cover_non_pesato_4_simple_DRD(G,PL_path,"gurobi")
    t_1 = time.time()
    delta_time = t_1 - t_0
    cover_opt_val = len(algo_4[0])
    status = algo_4[1]
    timeout = False
    problems = False

    if status == 1:
        timeout = True

    if status == 2:
        problems = True

    algo_list = [cover_opt_val,delta_time, timeout, problems]
    list_total.append(algo_list)

    # Algoritmo 4 con DRD e cutting plane
    t_0 = time.time()
    algo_4_bis = vertex_cover_non_pesato_4_OCI_cutting_plane(G)
    t_1 = time.time()
    delta_time = t_1 - t_0
    cover_opt_val = len(algo_4_bis[0])
    status = algo_4_bis[1]
    timeout = False
    problems = False

    if status == 1:
        timeout = True

    if status == 2:
        problems = True

    algo_list = [cover_opt_val, delta_time, timeout, problems]
    list_total.append(algo_list)

    # Algoritmo 5

    t_0 = time.time()
    algo_5 = vertex_cover_non_pesato_duale_5(G)
    t_1 = time.time()
    delta_time = t_1 - t_0
    cover_opt_val = len(algo_5)
    timeout = False
    problems = False
    algo_list = [cover_opt_val, delta_time, timeout, problems]
    list_total.append(algo_list)

    return list_total


def run_benchmark_on_list(graphs_list, PLI_path, PL_path):
    num_algos = 7
    tot_times = [0.0] * num_algos
    tot_ratios = [0.0] * num_algos
    has_timeout = [False] * num_algos
    has_problems = [False] * num_algos

    valid_instances = 0

    for G in graphs_list:
        # Se il grafo non è vuoto
        if G.number_of_edges() != 0:
            results = benchmark_np(G, PLI_path, PL_path)

            # Dal PLI:
            pli_size = results[0][0]
            pli_problems = results[0][3]

            # Ignoro i crash
            if not pli_problems:
                valid_instances += 1

                # Uso incumbent
                opt_size = pli_size
                if opt_size == 0: # capita solo nel caso di errori inaspettati, altrimenti il vincolo di cover porta ad avere almeno un vertice
                    opt_size = 1

                # Statistiche per ogni algoritmo
                for i in range(num_algos):
                    size, time_exec, timeout, problems = results[i]

                    tot_times[i] += time_exec

                    # Se timeout è True, has_timeout diventa True e resta True per sempre
                    has_timeout[i] = has_timeout[i] or timeout
                    has_problems[i] = has_problems[i] or problems

                    # Accumulo rapporto
                    tot_ratios[i] += (size / opt_size)

    # Calcolo medie finali
    summary = []
    if valid_instances > 0:
        for i in range(num_algos):
            avg_ratio = tot_ratios[i] / valid_instances
            avg_time = tot_times[i] / valid_instances
            # Aggiungiamo alla lista i flag persistenti (che saranno True se è successo almeno una volta)
            summary.append([avg_ratio, avg_time, has_timeout[i], has_problems[i]])

    return summary





def salva_benchmark_in_pdf(summary, nome_classe, pdf_obj):

    # Prende in input il risultato della run_benchmark_on_list
    # **************** il nome della classe considerata
    # **************** pdf_obj file pdf

    # Nomi degli algoritmi
    algo_names = ["PLI", "Algo_1", "Algo_2", "Algo_3", "DRD", "Cut&DRD", "Duale"]

    ratios = [row[0] for row in summary]
    times = [row[1] for row in summary]

    colors = ['blue' if row[3] else ('red' if row[2] else 'green') for row in summary]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"Benchmark: {nome_classe}", fontsize=16)

    # Plot Ratios
    ax1.bar(algo_names, ratios, color=colors, edgecolor='black', alpha=0.7)
    ax1.set_title("Rapporto di Approssimazione Medio")
    ax1.set_ylabel("Ratio (Alg / PLI)")
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Plot Times
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

    # SALVATAGGIO NELL'OGGETTO PDF APERTO
    pdf_obj.savefig(fig)

    # CHIUSURA FIGURA (Fondamentale per liberare RAM)
    plt.close(fig)





def crea_grafo_da_riga(row):

    n = int(row['nodi_effettivi'])
    edges = ast.literal_eval(row['lista_archi'])
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    return G


def overall_n_p(PLI_path, PL_path, CSV_path):
    print("Apertura del file PDF unico ('Report_Benchmark_Totale.pdf')...")
    # Apriamo il PDF assegnandolo a una variabile
    pdf = PdfPages('Report_Benchmark_Totale.pdf')

    try:
        # Leggiamo il CSV a blocchi di 15 per rispettare la struttura del tuo dataset
        reader = pd.read_csv(CSV_path, chunksize=15)

        for i, chunk in enumerate(reader):
            # IL TRUCCO: Prendiamo solo le prime 10 righe del chunk, le altre 5 vengono scartate
            chunk_10 = chunk.iloc[:10]

            row = chunk_10.iloc[0]
            nome_classe = f"N:{row['n_target']} | D:{row['d_target']} | C:{row['classe']}"

            print(f"Processando {nome_classe} (Batch {i + 1} - Analizzo 10 istanze su 15)...")

            list_graphs = [crea_grafo_da_riga(r) for _, r in chunk_10.iterrows()]

            # Lanciamo il benchmark
            summary = run_benchmark_on_list(list_graphs, PLI_path, PL_path)

            # Salva i grafici come una NUOVA PAGINA nel PDF aperto
            salva_benchmark_in_pdf(summary, nome_classe, pdf)

        print("\n--- Benchmark completato con successo su tutto il dataset! ---")

    except KeyboardInterrupt:
        print("\n!!! Esecuzione interrotta manualmente !!!")
        print("Chiusura di emergenza in corso: salvo le pagine generate finora...")

    except Exception as e:
        print(f"\n!!! Errore imprevisto durante il batch {i + 1}: {e} !!!")

    finally:
        pdf.close()
        print("File 'Report_Benchmark_Totale.pdf' chiuso e salvato in modo sicuro.")