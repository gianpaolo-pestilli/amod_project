import csv
from generatore_non_pesato import genera_singola_istanza


def starter_n_p():
    num_vertici = [50, 100, 200, 400, 800]
    densita_grafo = [0.2, 0.5, 0.8]
    classi = [0, 1, 2]

    lista_combinazioni = []
    for n in num_vertici:
        for d in densita_grafo:
            for c in classi:
                appo = [n, d, c]
                lista_combinazioni.append(appo)

    return lista_combinazioni


def writer_on_file(lista_combinazioni):
    nome_file = 'dataset_non_pesato.csv'

    with open(nome_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(
            ['n_target', 'd_target', 'classe', 'id_istanza', 'nodi_effettivi', 'archi_effettivi', 'lista_archi'])

        for combinazione in lista_combinazioni:
            n = combinazione[0]
            d = combinazione[1]
            c = combinazione[2]

            print(f"Generazione in corso: N={n}, D={d}, Classe={c}")

            for id_istanza in range(1, 16):
                G = genera_singola_istanza(n, d, c)

                nodi_effettivi = G.number_of_nodes()
                archi_effettivi = G.number_of_edges()

                lista_archi_str = str(list(G.edges()))

                writer.writerow([n, d, c, id_istanza, nodi_effettivi, archi_effettivi, lista_archi_str])

    totale_istanze = len(lista_combinazioni) * 15
    print(f"\nGenerazione completata! File '{nome_file}' salvato.")
    print(f"Istanze fisiche scritte nel CSV: {totale_istanze}")


def main():
    writer_on_file(starter_n_p())

if __name__ == "__main__":
    main()