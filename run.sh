#!/bin/bash


clear(){
    rm -rf logs/*
}

run_llama() {
  for i in {1..10}
  do
    ./llama-cli -fa -m models/llama2_7b_chat_uncensored-q4_0.gguf -p "The meaning" > ./logs/fa.log 2>&1
    tail -n 5 ./logs/fa.log >> ./logs/last_lines.log

    # # ./llama-cli -m models/meta-llama-3-8b-instruct.Q4_K_M.gguf -p "The meaning "> ./logs/nofa.log 2>&1
    # ./llama-cli -m models/llama2_7b_chat_uncensored-q4_0.gguf  -p "The meaning" > ./logs/nofa.log 2>&1
    # tail -n 5 ./logs/nofa.log >> ./logs/last_lines.log
    
  done
  echo "ten times finished"
}


# python grep.py
run_llama


 