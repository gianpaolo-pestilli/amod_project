# In questo file c'è il codice con cui ho scelto il massimo numero di nodi da testare

# L'idea è:
# Incremento il numero di nodi su un grafo completo finché
# almeno uno tra i 4 solver che ho scelto impiega più di 5 min a trovare l'ottimo

# Il test verrà effettuato sul problema di vertex cover non pesato.
# L'idea è che avere dei costi sia intrinsecamente più complesso rispetto a non averli
import multiprocessing
import networkx as nx
import time
from amplpy import AMPL


def worker_solve(model_path, solver_name, n, result_queue):
    try:
        ampl = AMPL()
        ampl.read(model_path)
        ampl.setOption("solver", solver_name)
        ampl.setOption("timelimit", 300)
        G = nx.complete_graph(n)
        ampl.set["V"] = list(G.nodes())
        ampl.set["E"] = list(G.edges())
        ampl.param["c"] = {node: 1 for node in G.nodes()}
        ampl.solve()
        status = ampl.get_value("solve_result")
        result_queue.put({"success": True, "status": status})
    except Exception as e:
        result_queue.put({"success": False, "error": str(e)})


def trova_limite_nodi(model_path, start_n=0, step=100, max_n=2000):
    solvers = ['cplex', 'gurobi', 'highs', 'scip']

    for n in range(start_n, max_n + step, step):
        print("Testando Grafo Completo con N = " + str(n))

        for s in solvers:
            queue = multiprocessing.Queue()
            p = multiprocessing.Process(target=worker_solve, args=(model_path, s, n, queue))
            p.start()
            p.join(timeout=310)
            # Se dopo 310 secondi non ha finito bisogna troncare
            if p.is_alive():
                print("Il solver " +s+ " ha superato il tempo limite totale. Terminazione forzata!")
                p.terminate()  # Kill del processo
                p.join()
                return n - step  # Restituisco l'ultimo N valido

            # Prendo il risultato dalla coda
            result = queue.get()

            if not result["success"]:
                print("Il solver" +s+ " ha riportato un errore: "+ result['error'])
                return n - step

            if result["status"] != 'solved':
                print("Il solver "+s+ " non ha raggiunto l'ottimo. Status: "+ result['status'])
                return n - step

            print("Solver " +s+ " ok...")

    return max_n


if __name__ == '__main__':

    percorso_modello = "C:\\Users\\tpest\\Desktop\\AMOD_project\\Codice\\vertex_cover.mod"

    print("Avvio stress-test per determinare il limite di N...")
    limite = trova_limite_nodi(percorso_modello)

    print("\n--- RISULTATO FINALE ---")

    print("Il limite massimo di vertici gestibile da tutti i solver è: " + str(limite))

