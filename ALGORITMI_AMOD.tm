<TeXmacs|2.1.4>

<style|<tuple|generic|italian>>

<\body>
  <with|font-series|bold|Vertex cover pesato e non>

  <with|font-series|bold|Grafo G = (V, E)>

  <hrule>

  <with|font-shape|italic|Tramite solver:>

  <with|font-series|bold|Modello PLI vertex cover non pesato:>

  min <big|sum><rsub|u \<in\> V> x<rsub|u>

  x<rsub|u> + x<rsub|v> \<geq\> 1 \<forall\> (u,v) \<in\> E

  x<rsub|u> \<in\> {0,1} \<forall\> u \<in\> V

  \;

  <with|font-series|bold|Modello PLI vertex cover pesato:>

  min <big|sum><rsub|u \<in\> V> c<rsub|u>x<rsub|u>

  x<rsub|u> + x<rsub|v> \<geq\> 1 \<forall\> (u,v) \<in\> E

  x<rsub|u> \<in\> {0,1} \<forall\> u \<in\> V

  <hrule>

  <with|font-series|bold|Algoritmo vertex cover non pesato 1 (partendo da un
  vertice qualunque):>

  1. C = {}; #cover

  2. I = E; #archi \Pscoperti\Q

  3. for v in V {

  4. C.insert(v);

  5. I = I / \<delta\>(v);

  6. if (I.isEmpty) then return C;

  7. }

  \;

  <with|font-series|bold|Algoritmo vertex cover pesato 1 (adattato da me,
  partendo dal vertice di peso minimo):>

  1. C = {}; #cover

  2. I = E; #archi \Pscoperti\Q

  3. W = sort_by_weight(V); #vertici ordinati per peso crescente

  4. for v in W {

  5. C.insert(v);

  6. I = I / \<delta\>(v);

  7. if (I.isEmpty) then return C;

  8. }

  \;

  \;

  \;

  \;

  <\with|font-series|bold>
    Algoritmo vertex cover non pesato 2 (ordinando i vertici per grado
    decrescente):
  </with>

  1. C = {}; #cover

  2. I = E; #archi \Pscoperti\Q

  3. W = sort_by_deg(V); #vertici ordinati per grado decrescente

  3. for v in W {

  4. C.insert(v);

  5. I = I / \<delta\>(v);

  6. if (I.isEmpty) then return C;

  7. }

  \;

  <with|font-series|bold|Algoritmo vertex cover pesato 2 (adattato da me,
  ordinando i vertici per grado e <underline|peso>):>

  1. C = {}; #cover

  2. I = E; #archi \Pscoperti\Q

  3. W = sort_by_deg_and_weight(V); #vertici ordinati per grado decrescente

  3. for v in W {

  4. C.insert(v);

  5. I = I / \<delta\>(v);

  6. if (I.isEmpty) then return C;

  7. }

  \;

  \;

  <\with|font-series|bold>
    Algoritmo vertex cover non pesato 3 (matching massimale):
  </with>

  1. C = {}; #cover

  2. I = E; #archi \Pscoperti\Q

  3. while( ! I.isEmpty){

  4. e = I[0]; #prendo un arco scoperto

  5. u = first_vertex(e);

  6. v = second_vertex(e);

  7. C.insert(u);

  8. C.insert(v);

  9. J = e \<cup\> \<delta\>(u) \<cup\> \<delta\>(v);

  10. I = I / J;

  11. }

  12. return C;

  \;

  \;

  <\with|font-series|bold>
    Algoritmo vertex cover pesato 3 (adattato da me, matching massimale):
  </with>

  1. C = {}; #cover

  2. I = E; #archi \Pscoperti\Q

  3. while( ! I.isEmpty){

  4. W = sort_by_weight(I); #ordino gli e = (u,v) \<in\> E in ordine
  crescente di c<rsub|u> + c<rsub|v>

  5. e = W[0]; #prendo il minimo arco scoperto

  6. u = first_vertex(e);

  7. v = second_vertex(e);

  8. C.insert(u);

  9. C.insert(v);

  10. J = e \<cup\> \<delta\>(u) \<cup\> \<delta\>(v);

  11. I = I / J;

  12. }

  13. return C;

  \;

  <\with|font-series|bold>
    Algoritmo vertex cover non pesato 4 (doubling and rounding down):
  </with>

  1. <with|font-shape|italic|Risolvo il problema rilassato:>

  min <big|sum><rsub|u \<in\> V> x<rsub|u>

  x<rsub|u> + x<rsub|v> \<geq\> 1 \<forall\> (u,v) \<in\> E

  x<rsub|u> \<geq\> 0 \<forall\> u \<in\> V<with|font-series|bold|>

  \;

  2. w = 0<rsup|\|V\|>;

  3. for (i \<leftarrow\> 1 to \|V\|) {

  4. if(x<rsub|i>* \<geq\> <frac|1|2>) then w<rsub|i> = 1;

  5. }

  6. return w

  \;

  <with|font-series|bold|Algoritmo vertex cover pesato 4 (adattato da me,
  doubling and rounding down):>

  1. <with|font-shape|italic|Risolvo il problema rilassato:>

  min <big|sum><rsub|u \<in\> V> c<rsub|u>x<rsub|u>

  x<rsub|u> + x<rsub|v> \<geq\> 1 \<forall\> (u,v) \<in\> E

  x<rsub|u> \<geq\> 0 \<forall\> u \<in\> V<with|font-series|bold|>

  \;

  2. w = 0<rsup|\|V\|>;

  3. for (i \<leftarrow\> 1 to \|V\|) {

  4. if(x<rsub|i>* \<geq\> <frac|1|2>) then w<rsub|i> = 1;

  5. }

  6. return w

  \;

  <with|font-series|bold|Algoritmo vertex cover non pesato (basato sul duale,
  adattato da me impostando tutti i pesi a 1):>

  1. x = 0<rsup|\|V\|>;

  2. y = \|0\|<rsup|\|E\|>;

  3. I = E; #archi \Pscoperti\Q

  4. while(x != vertex_cover(G)){

  5. e = I[0]; #prendo un arco scoperto

  6. u = first_vertex(e);

  7. v = second_vertex(e);\ 

  8. increment_u = 1 - <big|sum><rsub|e \<in\> \<delta\>(u)>y<rsub|e>;

  9. increment_v = 1 - <big|sum><rsub|e \<in\> \<delta\>(v)>y<rsub|e>;

  10. if(increment_u \<less\> increment_v) then {

  11. y<rsub|e> = \ 0;

  12. x<rsub|u> = 1;

  13. I = I / \<delta\>(u);

  14. } else if(increment_u \<gtr\> increment_v){

  15. y<rsub|e> = \ 0;

  16. x<rsub|v> = 1;

  17. I = I / \<delta\>(v);

  18. } else {

  19. #posso scegliere uno dei due

  20. y<rsub|e> = \ increment_u; #poiché sono uguali

  21. if(deg(u) \<leq\> deg(v)){ # scelgo il vertice con il grado maggiore

  22. x<rsub|v> = 1;

  23. I = I / \<delta\>(v);

  24. } else {

  25. x<rsub|u> = 1;

  26. I = I / \<delta\>(u);

  27. }

  28. }

  29. }

  30. return x;

  \;

  <\with|font-series|bold>
    Algoritmo vertex cover pesato (basato sul \Pduale\Q):
  </with>

  1. x = 0<rsup|\|V\|>;

  2. y = \|0\|<rsup|\|E\|>;

  3. I = E; #archi \Pscoperti\Q

  4. while(x != vertex_cover(G)){

  5. e = I[0]; #prendo un arco scoperto

  6. u = first_vertex(e);

  7. v = second_vertex(e);\ 

  8. increment_u = c<rsub|u> - <big|sum><rsub|e \<in\>
  \<delta\>(u)>y<rsub|e>;

  9. increment_v = c<rsub|v> - <big|sum><rsub|e \<in\>
  \<delta\>(v)>y<rsub|e>;

  10. if(increment_u \<leq\> increment_v) then {

  11. y<rsub|e> = \ increment_u;

  12. x<rsub|u> = 1;

  13. I = I / \<delta\>(u);

  14. } else {

  15. y<rsub|e> = \ increment_v;

  16. x<rsub|v> = 1;

  17. I = I / \<delta\>(v);

  18. }

  19. }

  20. return x;

  \;

  \;

  <with|font-shape|italic|Gianpaolo Pestilli>

  \;

  \;

  \;

  \;
</body>

<\initial>
  <\collection>
    <associate|page-medium|paper>
  </collection>
</initial>