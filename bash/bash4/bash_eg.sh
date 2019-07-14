#!/bin/bash

##6 element array used for returning values from functions:
RET_ARR[0]="A"
RET_ARR[1]="B"
RET_ARR[2]="C"
RET_ARR[3]="D"

function MULTI_RETURN(){
	##GIVE POSITIONAL ARGUMENTS/INPUTS $1 & $2 SOME SENSIBLE NAMES
	local out_dex_1="$1"
	local out_dex_2="$2"
	
	##Echo for debug
	echo "running: MULTI_RETURN"
	
	## Here: Calculate output values:
	local op_var_1="Hello"
	local op_var_2="World"
	
	RET_ARR[ $out_dex_1 ]=$op_var_1
	RET_ARR[ $out_dex_2 ]=$op_var_2
}

fn="MULTI_RETURN"
out_dex_a=0
out_dex_b=1
eval $fn $out_dex_a $out_dex_b		## <--- call function
a=${RET_ARR[0]} && echo "RET_ARR[0]: $a "
b=${RET_ARR[1]} && echo "RET_ARR[1]: $b "
echo
##-------------------------------------------##
