#!/usr/bin/env bash


while getopts ":d:s:l" OPT; do
  case $OPT in
    d)  MF=$OPTARG
        ;;
    s)  MET=$OPTARG
        ;;
    l)  PROG=$OPTARG
        ;;	
    esac
done
shift $((OPTIND -1))


for PROG in compilador.log matriz.log simulador.log compressor.log; do
for MET in lru new; do
  for MF in 128 516 1024 4096 16384; do
    >&2 echo $"----------------//-----------------"
    ./tp2virtual $MET $PROG 4 $MF >> resultsfixedpage.csv
  done
done
done

