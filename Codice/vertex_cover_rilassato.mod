# Modello: WEIGHTED VERTEX COVER
# Per il Vertex Cover non pesato utilizzerò lo stesso modello con tutti i pesi pari a 1

# Vertici
set V;

# Lati
set E within {V,V};

# Pesi di ciascun vertice
param c {V} >= 0;

# Variabili rilassate (rilassamento lineare)
var x {V} >= 0;

# Funzione obiettivo
minimize Peso_Complessivo:
    sum {u in V} c[u] * x[u];

# Vincoli di cover
subject to Vincolo_Cover {(u,v) in E}:
    x[u] + x[v] >= 1;
