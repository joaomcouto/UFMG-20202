#!/usr/bin/env bash


while getopts ":d:s:l" OPT; do
  case $OPT in
    d)  PG=$OPTARG
        ;;
    s)  MET=$OPTARG
        ;;
    l)  PROG=$OPTARG
        ;;	
    esac
done
shift $((OPTIND -1))


for PROG in compilador.log matriz.log simulador.log compressor.log; do
for MET in fifo lru; do
  for PG in 4 8 16 32 64; do
    >&2 echo $"----------------//-----------------"
    ./tp2virtual $MET $PROG $PG 16384 >> resultsfixedMF.csv
  done
done
done


