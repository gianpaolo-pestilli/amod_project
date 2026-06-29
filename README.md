
# Minimum Vertex Cover — Algoritmi di Approssimazione

**Progetto AMOD 2025-2026** · Gianpaolo Pestilli (matricola 0386492)

---

## Descrizione

Questo progetto implementa e confronta algoritmi di approssimazione per il problema del **Minimum Vertex Cover (MVC)**.

Lo studio valuta le prestazioni degli algoritmi in termini di **qualità della soluzione** (rapporto di approssimazione rispetto all'ottimo PLI) e **tempo di esecuzione**.
---

## Struttura del repository

```
amod_project/
├── Codice/
│   ├── algoritmi_non_pesato.py              # Algoritmi di approssimazione (caso non pesato)
│   ├── algoritmi_pesato.py                  # Algoritmi di approssimazione (caso pesato)
│   ├── generatore_non_pesato.py             # Generatore di istanze grafi non pesati
│   ├── generatore_pesato.py                 # Generatore di istanze grafi pesati
│   ├── starter_non_pesato.py                # Entry point: genera il dataset non pesato
│   ├── starter_pesato.py                    # Entry point: genera il dataset pesato
│   ├── raccolta_non_pesato.py               # Raccolta e salvataggio risultati (non pesato)
│   ├── raccolta_pesato.py                   # Raccolta e salvataggio risultati (pesato)
│   ├── benchmark_non_pesato.py              # Benchmark e grafici (non pesato)
│   ├── benchmark_pesato.py                  # Benchmark e grafici (pesato)
│   ├── vertex_cover.mod                     # Modello AMPL per il PLI (Weighted Vertex Cover)
│   ├── vertex_cover_PLI.py                  # Interfaccia Python al solver PLI (Gurobi/AMPL)
│   └── vertex_cover_rilassato.mod           # Modello AMPL per il rilassamento lineare
├── 0386492-Benchmark_NON_PESATO.pdf         # Report benchmark caso non pesato
├── 0386492-Benchmark_PESATO.pdf             # Report benchmark caso pesato
└── Presentazione_progetto_0386492.pdf       # Presentazione del progetto

```

---

## Come eseguire

### 1. Generare i dataset

```bash
cd Codice
python starter_non_pesato.py   # genera dataset_non_pesato.csv
python starter_pesato.py       # genera dataset_pesato.csv
```

### 2. Raccogliere i risultati

```bash
python raccolta_non_pesato.py  # esegue tutti gli algoritmi e salva i risultati
python raccolta_pesato.py
```

### 3. Produrre i benchmark

```bash
python benchmark_non_pesato.py  # genera grafici e report PDF
python benchmark_pesato.py
```

---

## Risultati

I report completi del benchmark sono disponibili nei file PDF inclusi nel repository:

- `0386492-Benchmark_NON_PESATO.pdf`
- `0386492-Benchmark_PESATO.pdf`

La presentazione di sintesi è disponibile in `Presentazione_progetto_0386492.pdf`.

---

## Autore

**Gianpaolo Pestilli** — Matricola 0386492  
Corso di Algoritmi e Metodi di Ottimizzazione Discreta (AMOD), A.A. 2025-2026