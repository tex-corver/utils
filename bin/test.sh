#!/bin/bash

scopes=()
path=()
while getopts "uiehp:" option; do
  case "${option}" in
  u)
    scopes+=("unit")
    ;;
  i)
    scopes+=("integration")
    ;;
  e)
    scopes+=("e2e")
    ;;
  p)
    path=${OPTARG}
    ;;
  *)
    echo $option
    ;;
  esac
done

if [ "${#scopes[@]}" == 0 ]; then
  scopes=("unit" "integration" "e2e")
fi

if [ -z $path ]; then
  for i in ${!scopes[@]}; do
    echo ${scopes[i]}
    coverage run -m pytest tests/${scopes[i]} -vvv
  done
else
  coverage run -m pytest $path -vvv
fi
