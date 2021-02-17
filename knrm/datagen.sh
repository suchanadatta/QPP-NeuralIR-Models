COSIM=60
K=100
N=5

for n in $(seq 1 1 $N)
do
  cp /dev/null data/$n.txt
  for k in $(seq 1 1 $K)
  do
    printf "$k " >> data/$n.txt
    for i in $(seq 1 1 $COSIM)
      do
        printf "$(($RANDOM % 100)) " >> data/$n.txt
      done
      printf "\n" >> data/$n.txt
  done
done
