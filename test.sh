n_tests=$1
array_len=$2
num_threads=$3
echo Starting with parameters:
echo "$n_tests" tests
echo "$array_len" array length
echo "$num_threads" number of threads
all_times=()
for i in $(seq "$n_tests"); do
  echo -ne " $i" of "$n_tests" tests "\r"
  seconds=$(./cmake-build-debug/merge-sort "$array_len" 0 "$num_threads")
  all_times+=("$seconds")
done
echo Tests done. Calculating average time...
total=0
for item in "${all_times[@]}"; do
    total=$(echo print "${total}+${item}" | perl)
    # total=$(bc -l <<<"${total}+${item}")
  #  echo "$item" "$total"
done
echo Total time "$total" seconds
# avg=$(bc -l <<<"${total}/${n_tests}")
avg=$(echo print "${total}/${n_tests}" | perl)
echo Average time "$avg" seconds
printf "$n_tests $array_len $num_threads $avg\n" >> "$4"
