#!/bin/bash

#foldname = "grissom_fold_"

#for number in $(seq 100 10 100)
#do
#  echo "============ top docs : $number ============"
  trainFoldLocation="/store/causalIR/drmm/clueweb_exp/4-folds/cw09b.qrel_fold_1.train"
  trainHistogramLocation="/store/causalIR/drmm/clueweb_exp/qrel_histogram_30.txt"
  testFoldLocation="/store/causalIR/drmm/clueweb_exp/4-folds/cw09b.qrel_fold_1.test"
  testHistogramLocation="/store/causalIR/drmm/clueweb_exp/prerank_histogram_30.txt"
#  echo "============ test file input : "$testFoldLocation" ============"
#  python3 run_model.py "trec8_bin30_TD"$number "$trainFoldLocation" "$trainHistogramLocation" "$testFoldLocation" "$testHistogramLocation" #&> logs/fold1.log &
#done

python3 run_model.py "CW_bin30_TD1000" "$trainFoldLocation" "$trainHistogramLocation" "$testFoldLocation" "$testHistogramLocation" #&> logs/fold1.log &


#for number in $(seq 1 1 5)
#do
#	echo "running fold: $number"
#	python3 run_model.py "$foldname$number" "$trainFoldLocation$number.train" "$trainHistogramLocation" "$testFoldLocation$number.test" "$testHistogramLocation" #&> logs/fold1.log &
#done
#exit 0

#python3 run_model.py schirra_fold1 "../data/5-folds/robust04.qrels_fold_1.train" "../data/qrel_histogram_30.txt" "../data/5-folds/robust04.qrels_fold_1.test" "../data/prerank_histogram_30.txt" #&> logs/fold1.log &
#
#python3 run_model.py schirra_fold2 "../data/5-folds/robust04.qrels_fold_2.train" "../data/qrel_histogram_30.txt" "../data/5-folds/robust04.qrels_fold_2.test" "../data/prerank_histogram_30.txt" #&> logs/fold2.log &
#python3 run_model.py schirra_fold3 "../data/5-folds/robust04.qrels_fold_3.train" "../data/qrel_histogram_30.txt" "../data/5-folds/robust04.qrels_fold_3.test" "../data/prerank_histogram_30.txt" #&> logs/fold3.log &
#python3 run_model.py schirra_fold4 "../data/5-folds/robust04.qrels_fold_4.train" "../data/qrel_histogram_30.txt" "../data/5-folds/robust04.qrels_fold_4.test" "../data/prerank_histogram_30.txt" #&> logs/fold4.log &
#python3 run_model.py schirra_fold5 "../data/5-folds/robust04.qrels_fold_5.train" "../data/qrel_histogram_30.txt" "../data/5-folds/robust04.qrels_fold_5.test" "../data/prerank_histogram_30.txt" #&> logs/fold5.log &
#
#
#wait

echo "all processes completed"