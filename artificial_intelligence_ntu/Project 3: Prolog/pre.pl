pre([],X).
pre([X|Y],[X|Z]):-pre(Y,Z).
