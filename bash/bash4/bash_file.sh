#!/bin/bash

function fun1(){
	echo 34
}
function fun2(){
	fun1
	local res=$?
	echo $res
}

a="2"
b="3"
fun1() 4 5
echo -e "Please enter your name: "
read name
echo "Nice to meet you $name"
