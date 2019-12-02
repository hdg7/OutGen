#!/bin/bash 

GENERATEPATHS=/home/menendez/projects/cvc4/genetic/generatePaths.sh
CLEANER=/home/menendez/data/eurystheus/eurystheus/visitors/pyVisitors/guardsCleanerMain.py

NAME=$(basename $1)
COUNTER=0
echo "program: $1"
echo "function: $2"
echo "cbmc $1 --unwind $3 --function $2 $4 > $NAME.output.txt"
cat $1
#CBMC generates the PCS for all possible paths up to an unwinding level.
#cbmc $1 --show-vcc --unwind 5 --function $2  > $NAME.output.txt
cbmc $1 --unwind $3 --function $2 $4 > $NAME.output.txt

#We need to translate the outputs to the solver, and at the same time identify Godel 
#constraints for our inputs
(cat $NAME.output.txt; printf "\n") | grep "^(" | grep -v "CPROVER" | grep -v "nondet_symbol" > $NAME.output.cvc
sed -i -e 's/!(/Not(/g' $NAME.output.cvc
sed -i -e 's/!\\/not \\/g' $NAME.output.cvc
sed -i -e 's/ASSUME//g' $NAME.output.cvc
sed -i -e 's/(signed long int)//g' $NAME.output.cvc
sed -i -e 's/(signed int)//g' $NAME.output.cvc
cat $NAME.output.cvc | cut -f2- -d' ' | tr '$!@#' '____' | sed -e 's/\([0-9]*\)l/\1/g' > $NAME.output.pre.clean.cvc
cat $NAME.output.pre.clean.cvc | grep -v return\' > $NAME.output.clean.cvc
cat $NAME.output.pre.clean.cvc | grep return\' | sed -e 's/\(.*\) == \(.*\)/retVal == \2/g' >> $NAME.output.clean.cvc
#Extracting guards and statements
cat $NAME.output.clean.cvc | grep "guard" | sed -e 's/\\guard/guard/g' | sed -e 's/&&/and/g' | sed -e "s/||/or/g" | tr -d "'"> $NAME.output.guards.cvc
cat $NAME.output.clean.cvc | grep -v "guard" | sed -e 's/&&/and/g' | sed -e "s/||/or/g" |  tr -d "'" > $NAME.output.statements.cvc
#Getting variables and constructing their definition
grep -o -E '\w+'< $NAME.output.clean.cvc | grep -v -E '^[0-9]+$' | sort | uniq | grep -v "not" | grep -v "Not" > $NAME.output.variables.cvc
#echo "retVal" >> $NAME.output.variables.cvc
cat $NAME.output.variables.cvc | grep guard | tr '\n' ',' | sed 's/,$/,Bools\n/'  > $NAME.output.declar.cvc
cat $NAME.output.variables.cvc | grep -v guard | tr '\n' ',' | sed 's/,$/,Ints\n/' >> $NAME.output.declar.cvc
cat $NAME.output.variables.cvc | grep guard > $NAME.output.all.guards
#Extract the inputs
#sh ../extractInputs.sh $NAME.output
#Statement construction
cat $NAME.output.statements.cvc > $NAME.output.statementsASSERTS.cvc
cat $NAME.output.statementsASSERTS.cvc  | grep -v '?' > $NAME.output.pre.statementsASSERTS.cvc
cat $NAME.output.statementsASSERTS.cvc |  grep '?' | sed -e "s/\(.*\) == (\(.*\) ? \(.*\) : \(.*\))/Or(And(\2, \1 == \3),And(Not(\2), \1 == \4))/" >  $NAME.output.pre2.statementsASSERTS.cvc
cat  $NAME.output.pre.statementsASSERTS.cvc  $NAME.output.pre2.statementsASSERTS.cvc > $NAME.output.final.statementsASSERTS.cvc
#Cleaning guards
cat $NAME.output.guards.cvc | grep -v '?' > $NAME.output.guards.clean.cvc
cat $NAME.output.guards.cvc | grep '?' | sed -e "s/\(.*\) == (\(.*\) ? \(.*\) : \(.*\))/Or(And(\2, \1 == \3),And(Not(\2), \1 == \4))/" > $NAME.output.guards.complex.cvc
cat $NAME.output.guards.clean.cvc | grep -v "==" > $NAME.output.pcs.cvc
#Dealing with loops
cat $NAME.output.pcs.cvc | sed -e "s/And//g" |grep -o -E '\w+' | grep -v "Not" > $NAME.output.special.guards
cat $NAME.output.guards.clean.cvc | grep "==" | sed -e "s/\(guard_[0-9]*\) == \(.*\)/\1 == (\2)/"| sed -e "s/And/and/g" | sed -e "s/Not/not/g" | sed -e "s/Or/or/g" >> $NAME.output.guards.complex.cvc
python3 $CLEANER $NAME.output.guards.complex.cvc > $NAME.output.final.guards.cvc
#Finding the general guards where godel numbers can be added
#Constructing the final path after unlooping
cat $NAME.output.declar.cvc $NAME.output.final.statementsASSERTS.cvc $NAME.output.final.guards.cvc > $5
