import os
from benchmark_non_pesato import overall_n_p


def get_config_paths():
    base_dir = os.getcwd()
    config = {
        "PLI_path": os.path.join(base_dir, "vertex_cover.mod"),
        "PL_path": os.path.join(base_dir, "vertex_cover_rilassato.mod"),
        "CSV_path": os.path.join(base_dir, "dataset_non_pesato.csv")
    }
    return config


def main():
    paths = get_config_paths()
    missing_files = [k for k, v in paths.items() if not os.path.exists(v)]

    if missing_files:
        print(f"ERRORE: I seguenti file non sono stati trovati nella cartella {os.getcwd()}:")
        for f in missing_files:
            print(f" - {f}")
        return

    print("--- Avvio Benchmark ---")
    print(f"File PLI: {paths['PLI_path']}")
    print(f"File CSV: {paths['CSV_path']}")

    # 2. Lancio del benchmark
    try:
        overall_n_p(paths['PLI_path'], paths['PL_path'], paths['CSV_path'])
        print("\n--- Benchmark completato con successo! ---")
    except Exception as e:
        print(f"\n--- Errore durante l'esecuzione del benchmark: {e} ---")


if __name__ == "__main__":
    main()