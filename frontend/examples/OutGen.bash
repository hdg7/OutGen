#!/bin/bash

#Remember to set up the DFT home variable as:
#export DFT_HOME=/path/to/DFT


FILE=$1
FUNC=$2
ROOTDIR=$3
INPUTS=$4

cd $ROOTDIR
NAME=$(basename $FILE | cut -f1 -d'.')
mkdir $NAME
cp $FILE $NAME/
cd $NAME
NAME=$(basename $FILE)
cat $NAME | grep "#include" > $NAME.header
echo "#include <signal.h>
#include<stdlib.h>
#include<stdio.h>
#include<errno.h>
#include <unistd.h>
#include <sys/wait.h>
pid_t child_pid =-1 ;
int inst_flag=0;
void kill_child(int sig)
{
    kill(child_pid,SIGKILL);
}" >> $NAME.header
cat $NAME | grep -v "#include" > $NAME.1.c
gcc -E $NAME.1.c > $NAME.pre.c
python3 $DFT_HOME/frontend/preprocessing/prepro.py $NAME.pre.c $FUNC
if [ "$FUNC" == "main" ]; then
    FUNC=mainFake
fi
timeout 10 cbmc $NAME.pre.c.cbmc.c --unwind 5 --function $FUNC --z3 --outfile $NAME.z3
if [ -s $NAME.z3 ]
then
    rm *cov.c
    cat $NAME.z3 | sed -n '/(check-sat)/q;p' | sed 's/^;.*//g' | tr ':!@;!#&' '_______' | tail -n +5 > $NAME.clean.z3
    python3 $DFT_HOME/frontend/generation/gen.py outgen  $NAME.pre.c.cbmc.c  $NAME.pre.c.ori.c $FUNC $INPUTS $NAME.clean.z3
    #check from this!
    python3 $DFT_HOME/frontend/execution/set.inputs.py sem  $NAME.pre.c.ori.c $FUNC $NAME.pre.c.cbmc.c.inputs $INPUTS $RANDOM  
    cat $NAME.header  $NAME.pre.c.ori.c.cov.c > finalTest.c
    gcc -fprofile-arcs -ftest-coverage -lm finalTest.c
    ./a.out 2>&1 >/dev/null | sed 's/]]/ /g' | tr ' ' '\n' | grep REACHED | wc -l > count.txt
    gcov -fb finalTest.c > coverage.txt
fi


