rpcalc: rpcalc.l rpcalc.y rpcalc.h
	bison -d ./rpcalc.y
	flex ./rpcalc.l
	gcc -static ./lex.yy.c ./rpcalc.tab.c -lm -lfl -lgmp
