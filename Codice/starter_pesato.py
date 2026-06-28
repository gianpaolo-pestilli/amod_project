import csv
import networkx as nx
from generatore_pesato import genera_singola_istanza_pesata

def starter_pesato():
    num_vertici = [50, 100, 200, 400, 800]
    densita_grafo = [0.2, 0.5, 0.8]
    b_val = [10, 1000, 10000]
    spearman = [-1, 0, 1]

    lista_combinazioni = []
    for n in num_vertici:
        for d in densita_grafo:
            for b in b_val:
                for sp in spearman:
                    appo = [n, d, b, sp]
                    lista_combinazioni.append(appo)

    return lista_combinazioni

def writer_on_file_pesato(lista_combinazioni):
    nome_file = 'dataset_pesato.csv'

    with open(nome_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Intestazione
        writer.writerow(
            ['n_target', 'd_target', 'b_val', 'spearman', 'id_istanza',
             'nodi_effettivi', 'archi_effettivi', 'lista_archi', 'pesi_nodi']
        )

        for combinazione in lista_combinazioni:
            n = combinazione[0]
            d = combinazione[1]
            b = combinazione[2]
            sp = combinazione[3]

            print(f"Generazione in corso: N={n}, D={d}, B_val={b}, Spearman={sp}")

            for id_istanza in range(1, 16):

                G = genera_singola_istanza_pesata(n, d, b, sp)

                nodi_effettivi = G.number_of_nodes()
                archi_effettivi = G.number_of_edges()

                lista_archi_str = str(list(G.edges()))
                pesi_nodi = nx.get_node_attributes(G, 'peso')
                pesi_nodi_str = str(pesi_nodi)

                writer.writerow([
                    n, d, b, sp, id_istanza,
                    nodi_effettivi, archi_effettivi,
                    lista_archi_str, pesi_nodi_str
                ])

    totale_istanze = len(lista_combinazioni) * 15
    print(f"\n--- GENERAZIONE COMPLETATA ---")
    print(f"File '{nome_file}' salvato con successo.")
    print(f"Totale combinazioni esplorate: {len(lista_combinazioni)}")
    print(f"Istanze fisiche scritte nel CSV: {totale_istanze}")

def main():
    print("Avvio motore di generazione per grafo pesato...")
    combinazioni = starter_pesato()
    writer_on_file_pesato(combinazioni)

if __name__ == "__main__":
    main()