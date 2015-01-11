maxsum(L,X):-dp(L,0,0,X).
dp([],SUM,MAXSUM,X):- X is MAXSUM.
dp([H|L],SUM,MAXSUM,X):-
	H + SUM > MAXSUM -> dp(L, H+SUM, H+SUM, X);
	H + SUM > 0 -> dp(L, H+SUM, MAXSUM, X);
	dp(L, 0, MAXSUM, X).
