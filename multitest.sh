n_threads_array=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 60 70 80 90 100)
array_len=100000000
n_tests=100
rm out.txt
for n_threads in "${n_threads_array[@]}"; do
    ./test.sh $n_tests $array_len "$n_threads" out.txt
done
python analyze.py