append([],X,X).
append([H|X],Y,[H|Z]):-append(X,Y,Z).
rev([],[]).
rev(X,[H|Y]):-rev(Z,Y),append(Z,[H],X).
