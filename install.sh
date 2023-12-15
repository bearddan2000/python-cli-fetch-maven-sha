#!/usr/bin/env bash

function python-check() {
  local cmd=`python3 --version`

  if [ -z "$cmd" ]; then
    echo "python3 not installed"
  fi
}

function start-up(){
  python3 ./fetch.py
}

trap python-check 0

start-up