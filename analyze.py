import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

num_threads_array = []
avg_time_array = []

with open('out.txt', 'r') as f:
    for line in f.readlines():
        n_tests, array_len, num_threads, avg = line.split()
        # print(num_threads, avg)
        num_threads_array.append(int(num_threads))
        avg_time_array.append(round(float(avg), 3))

optimal_thread_num = min(zip(num_threads_array, avg_time_array), key=lambda x: x[1])
print(f"{optimal_thread_num[0]=}")

num_threads_array = np.array(num_threads_array)
avg_time_array = np.array(avg_time_array)

fig, axs = plt.subplots(2, 2)
fig.suptitle(f"{n_tests} tests, {array_len} length of array. {optimal_thread_num[0]} optimal thread num.  "+r"$S_p = \dfrac{1}{\alpha+\dfrac{1-\alpha}{p}} \Rightarrow \alpha=\dfrac{p-S_p}{(p-1)\cdot S_p} $")

polynom_rank = 20
original_data_line_width = .2
original_data_line_style='--'
approximate = True

axs[0, 0].plot(num_threads_array, avg_time_array, linestyle=original_data_line_style, linewidth=original_data_line_width)
if approximate:
    linear_model = np.polyfit(num_threads_array, avg_time_array, polynom_rank)
    linear_model_fn = np.poly1d(linear_model)
    axs[0, 0].plot(num_threads_array, linear_model_fn(num_threads_array), color="green")
axs[0, 0].plot(optimal_thread_num[0], optimal_thread_num[1], 'ro')
axs[0, 0].set_xscale('log', base=2)
axs[0, 0].xaxis.set_major_formatter(mtick.FormatStrFormatter('%g'))
axs[0, 0].set_xticks([2**i for i in range(8)]) # [1, 128]
axs[0, 0].set_title('$T$ - среднее время')
axs[0, 0].set_xlabel('$p$')
axs[0, 0].set_ylabel('$T$')

t1 = avg_time_array[0]
s = t1 / avg_time_array
axs[0, 1].plot(num_threads_array, s, linestyle=original_data_line_style, linewidth=original_data_line_width)
if approximate:
    linear_model = np.polyfit(num_threads_array, s, polynom_rank)
    linear_model_fn = np.poly1d(linear_model)
    axs[0, 1].plot(num_threads_array, linear_model_fn(num_threads_array), color="green")
axs[0, 1].plot(optimal_thread_num[0], s[optimal_thread_num[0]], 'ro')
axs[0, 1].set_title('$S_p$ - ускорение')
axs[0, 1].set_xscale('log', base=2)
axs[0, 1].xaxis.set_major_formatter(mtick.FormatStrFormatter('%g'))
axs[0, 1].set_xticks([2**i for i in range(8)]) # [1, 128]
axs[0, 1].set_xlabel('$p$')
axs[0, 1].set_ylabel('$S_p$')

alpha = (num_threads_array[1:] - s[1:]) / ((num_threads_array[1:] - 1) * s[1:])
axs[1, 0].plot(num_threads_array[1:], alpha, linestyle=original_data_line_style, linewidth=original_data_line_width)
if approximate:
    linear_model = np.polyfit(num_threads_array[1:], alpha, polynom_rank)
    linear_model_fn = np.poly1d(linear_model)
    axs[1, 0].plot(num_threads_array, linear_model_fn(num_threads_array), color="green")
axs[1, 0].plot(optimal_thread_num[0], alpha[optimal_thread_num[0]], 'ro')
axs[1, 0].set_ylim(0, max(alpha)*1.05)
axs[1, 0].set_xlim(2, max(num_threads_array))
axs[1, 0].set_xscale('log', base=2)
axs[1, 0].xaxis.set_major_formatter(mtick.FormatStrFormatter('%g'))
axs[1, 0].set_xticks([2**i for i in range(1,8)]) # [1, 128]
axs[1, 0].set_title(r'$\alpha$ - параллельная часть вычислений')
axs[1, 0].set_xlabel('$p$')
axs[1, 0].set_ylabel(r'$\alpha$')

efficiency = s / num_threads_array
axs[1, 1].plot(num_threads_array, efficiency, linestyle=original_data_line_style, linewidth=original_data_line_width)
if approximate:
    linear_model = np.polyfit(num_threads_array, efficiency, polynom_rank)
    linear_model_fn = np.poly1d(linear_model)
    axs[1, 1].plot(num_threads_array, linear_model_fn(num_threads_array), color="green")
axs[1, 1].plot(optimal_thread_num[0], efficiency[optimal_thread_num[0]], 'ro')
axs[1, 1].set_xscale('log', base=2)
axs[1, 1].xaxis.set_major_formatter(mtick.FormatStrFormatter('%g'))
axs[1, 1].set_xticks([2**i for i in range(8)]) # [1, 128]
axs[1, 1].set_title(r'$\frac{s_p}{p}$ - эффективность')
axs[1, 1].set_xlabel('$p$')
axs[1, 1].set_ylabel(r'$\frac{s_p}{p}$')

fig.set_size_inches(18.5, 10.5)
plt.tight_layout()
import time
filename=f"{array_len}_{n_tests}_{time.strftime('%Y%m%d-%H%M%S')}.png"
plt.savefig(filename, dpi=300)
# plt.show()
import os
os.system(f'xdg-open {filename}')
