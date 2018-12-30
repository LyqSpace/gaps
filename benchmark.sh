#!/bin/bash

test_n=3
nums=(20 30 40 60)
test=("doc0" "doc3" "doc7" "doc10" "doc11" "doc12" "doc13" "doc14" "doc15" "doc16" "doc17" "doc18" "doc19" "doc20" "doc21" "doc22")
test2=("doc23" "doc24")

if [ $# == 0 ]; then
    for var in ${test[@]}; do
        echo "Test case: "$var
        for i in $(seq 0 ${test_n}); do
            python3 ./bin/create_puzzle_stripe.py images/${var}.png --destination puzzles/${var}.png -n ${nums[i]}
            echo " "
            python3 ./bin/gaps_stripe.py --image puzzles/${var}.png -n ${nums[i]} --save
            echo " "
        done
    done
fi  

echo "Test case: "$1

for i in $(seq 0 ${test_n}); do
    python3 ./bin/create_puzzle_stripe.py images/$1.png --destination puzzles/$1.png -n ${nums[i]}
    echo " "
    python3 ./bin/gaps_stripe.py --image puzzles/$1.png -n ${nums[i]} --save
    echo " "
done
