#!/bin/bash

clear() {
  rm -rf logs/*
}

run_llama() {
  maxlen=30
  fa=0
  # model_name="meta-llama-3-8b-instruct.Q4_K_M.gguf"
  model_name="llama2_7b_chat_uncensored-q4_0.gguf"
  logfile="./logs/${model_name:0:6}${fa}fa${maxlen}.log"
  # for i in {1..5}; do
  for i in {1..2}; do
    if [ "$fa" == 1 ]; then
      ./llama-cli -fa -m models/$model_name -p "Tybalt encounters Mercutio and Romeo at the beach.  Mercutio intervenes and batters Tybalt, and is about to kill him when Romeo stops him. Tybalt takes the opportunity to fatally wound Mercutio, who curses both houses before dying. Enraged, Romeo chases after the fleeing Tybalt and shoots him dead, avenging Mercutio’s death.Captain Prince banishes Romeo from the city, and he goes into hiding with Father Laurence. The nurse arrives and tells him that Juliet is waiting for him. Romeo climbs Juliet's balcony and they consummate their marriage, with Romeo departing the next morning. The next morning, Gloria informs Juliet that she is to marry Paris, and when Juliet refuses, Fulgencio physically assaults her and threatens to disown her. Juliet runs away and seeks out Father Laurence, imploring him to help her, while threatening to commit suicide. Father Laurence gives her a potion that will let her fake her own death, after which she will be " -n $maxlen > ./logs/tmp.log 2>&1
      # ./llama-cli -fa -m models/$model_name -p "The weather in boston"  -n $maxlen > ./logs/tmp.log 2>&1
    else
      ./llama-cli -m models/$model_name -p "Tybalt encounters Mercutio and Romeo at the beach.  Mercutio intervenes and batters Tybalt, and is about to kill him when Romeo stops him. Tybalt takes the opportunity to fatally wound Mercutio, who curses both houses before dying. Enraged, Romeo chases after the fleeing Tybalt and shoots him dead, avenging Mercutio’s death.Captain Prince banishes Romeo from the city, and he goes into hiding with Father Laurence. The nurse arrives and tells him that Juliet is waiting for him. Romeo climbs Juliet's balcony and they consummate their marriage, with Romeo departing the next morning. The next morning, Gloria informs Juliet that she is to marry Paris, and when Juliet refuses, Fulgencio physically assaults her and threatens to disown her. Juliet runs away and seeks out Father Laurence, imploring him to help her, while threatening to commit suicide. Father Laurence gives her a potion that will let her fake her own death, after which she will be " -n $maxlen > ./logs/tmp.log 2>&1
      # ./llama-cli -m models/$model_name -p "The weather in boston" -n $maxlen > ./logs/tmp.log 2>&1
    fi
    tail -n 5 ./logs/tmp.log >> $logfile
  done
  grep "llama_new_context_with_model:      Metal compute buffer size =" ./logs/tmp.log >> $logfile
  echo "save to  $logfile"
  python grep.py $logfile
}

runop(){
  maxlen=30
  fa=0
  # model_name="meta-llama-3-8b-instruct.Q4_K_M.gguf"
  model_name="llama2_7b_chat_uncensored-q4_0.gguf"
  logfile="./logs/${model_name:0:6}${fa}fa${maxlen}.log"

  if [ "$fa" == 1 ]; then
    # ./llama-cli -fa -m models/$model_name -p "The weather in boston" -n $maxlen > $logfile 2>&1
    ./llama-cli -fa -m models/$model_name -n $maxlen -p "Tybalt encounters Mercutio and Romeo at the beach. Romeo attempts to make peace, but Tybalt assaults him. Mercutio intervenes and batters Tybalt, and is about to kill him when Romeo stops him. Tybalt takes the opportunity to fatally wound Mercutio, who curses both houses before dying. Enraged, Romeo chases after the fleeing Tybalt and shoots him dead, avenging Mercutio’s death.Captain Prince banishes Romeo from the city, and he goes into hiding with Father Laurence. The nurse arrives and tells him that Juliet is waiting for him. Romeo climbs Juliet's balcony and they consummate their marriage, with Romeo departing the next morning. The next morning, Gloria informs Juliet that she is to marry Paris, and when Juliet refuses, Fulgencio physically assaults her and threatens to disown her. Juliet runs away and seeks out Father Laurence, imploring him to help her, while threatening to commit suicide. Father Laurence gives her a potion that will let her fake her own death, after which she will be placed within the Capulet vault to awaken 24 hours later. Father Laurence vows to inform Romeo of the plot via overnight letter, whereupon the latter will sneak into the vault and, once reunited with Juliet and him." > $logfile 2>&1
  else
    ./llama-cli -m models/$model_name -p "The weather in boston" -n $maxlen > $logfile 2>&1
    # ./llama-cli -m models/$model_name -n $maxlen -p "Tybalt encounters Mercutio and Romeo at the beach. Romeo attempts to make peace, but Tybalt assaults him. Mercutio intervenes and batters Tybalt, and is about to kill him when Romeo stops him. Tybalt takes the opportunity to fatally wound Mercutio, who curses both houses before dying. Enraged, Romeo chases after the fleeing Tybalt and shoots him dead, avenging Mercutio’s death.Captain Prince banishes Romeo from the city, and he goes into hiding with Father Laurence. The nurse arrives and tells him that Juliet is waiting for him. Romeo climbs Juliet's balcony and they consummate their marriage, with Romeo departing the next morning. The next morning, Gloria informs Juliet that she is to marry Paris, and when Juliet refuses, Fulgencio physically assaults her and threatens to disown her. Juliet runs away and seeks out Father Laurence, imploring him to help her, while threatening to commit suicide. Father Laurence gives her a potion that will let her fake her own death, after which she will be placed within the Capulet vault to awaken 24 hours later. Father Laurence vows to inform Romeo of the plot via overnight letter, whereupon the latter will sneak into the vault and, once reunited with Juliet and him." > $logfile 2>&1
  fi

  echo "save to  $logfile"
  python grep.py $logfile
}

clear
run_llama
# runop
