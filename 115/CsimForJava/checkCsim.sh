while [ 1 ]
do
  if ssh -i ~/.ssh/openlab jalbert1@openlab.ics.uci.edu "module avail -t 2>&1 | grep -i csim 1>/dev/null";
    then
      echo $(ssh -i ~/.ssh/openlab jalbert1@openlab.ics.uci.edu  "hostname") >> hostnames
  else
    echo $(ssh -i ~/.ssh/openlab jalbert1@openlab.ics.uci.edu  "hostname") >> not_hostnames
  fi
done
