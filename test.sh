#!/bin/bash

# Run the first command and redirect stdout and stderr to fa.log
./llama-cli -fa -m models/llama2_7b_chat_uncensored-q4_0.gguf  -p "The meaning" > ./logs/fa.log 2>&1
# ./llama-cli -m models/meta-llama-3-8b-instruct.Q4_K_M.gguf -p "The meaning "> ./logs/nofa.log 2>&1
echo "fa finished"
# Run the second command and redirect stdout and stderr to nofa.log
./llama-cli -m models/llama2_7b_chat_uncensored-q4_0.gguf  -p "The meaning" > ./logs/nofa.log 2>&1
echo "nofa finished"
python grep.py
 
 