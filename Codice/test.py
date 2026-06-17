from amplpy import AMPL

ampl = AMPL()

# --- MODIFICA QUESTE DUE RIGHE ---
ampl.option["solver"] = "gurobi"
ampl.option["cplex_options"] = "outlev=1"  # Accende il log di CPLEX
# ---------------------------------

print("--- COSTRUZIONE MODELLO GIGANTE ---")
ampl.eval("""
    var x{1..500000} >= 0;
    maximize obiettivo: sum{i in 1..500000} x[i];
    s.t. vincoli{i in 1..500000}: x[i] <= 2;
""")

print("--- AVVIO  ---")
ampl.solve()

risultato = ampl.get_objective('obiettivo').value()

print(f"\nRisultato atteso: 10000.0")
print(f"Risultato ottenuto: {risultato}")