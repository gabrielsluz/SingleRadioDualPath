
set N; # Nos
set O; # Origem
set D; # Destino
set NotD := N diff D; # Nos que nao sao destino
set NotOD := NotD diff O; # Nos que nao sao origem nem destino

set A within N cross N; # Arestas
set S{i in N} := {j in N: (i,j) in A}; # Saída
set E{i in N} := {j in N: (j,i) in A}; # Entrada

# for{i in N} for {j in S[i]} printf "S[%d] %d\n", i,j;
# for{i in N} for {j in E[i]} printf "E[%d] %d\n", i,j;

param c{A}; # Custo

var x{A}, binary;


minimize obj: sum{(i,j) in A} (c[i,j] * x[i,j]);

# Conservacao do Fluxo
s.t. cons1O1{i in O}: sum{j in S[i]} x[i,j] = 2;
s.t. cons1O2{i in O}: sum{j in E[i]} x[j,i] = 0;
s.t. cons1NotOD{i in NotOD}: sum{j in S[i]} x[i,j] - sum{j in E[i]} x[j,i] = 0;
s.t. cons1D1{i in D}: sum{j in S[i]} x[i,j] = 0;
s.t. cons1D2{i in D}: sum{j in E[i]} x[j,i] = 2;


# Apenas 1 radio
s.t. umradio{i in NotD}: sum{j in E[i]} x[j,i] <= 1;

#Output para simulacao
s.t. Sim{(i,j) in A}: x[i,j]*c[i,j] <= c[i,j];

end;
