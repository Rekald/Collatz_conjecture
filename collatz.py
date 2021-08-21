#########################################################
#                                                       #
#       Collatz conjecture algorithm:                   #
#      -Starting from a positive integer number         #
#      -If the number is even, divide it by two         #
#      -If the number is odd, triple it and add one     #
#      -If the number equals 1, the algoritmh ends      #
#                                                       #
#########################################################

import glob
import os
import datetime
import matplotlib.pyplot as plt
from threading import Thread as Th
#from multiprocessing import Process

PROGRAM_STATE = {1: True, 2: False}
THREAD_MAX_NUM = 5
THREADS_ARGS = {0: 0, 1: -1, 2: 1, 3: -2, 4: 2}
DIRNAME = "testfiles"
FILENAME = "_Test.txt"
MULTIPLOT = 0

def collatz_num(n, subdir_name):
    with open(f"{DIRNAME}/{subdir_name}/{str(int(n)) + FILENAME}", "w") as fout:
        fout.write(str(int(n)))
        while n != 1:
            fout.write(", ")
            if n % 2 == 0:
                n = int(n / 2)
            else:
                n = (n * 3) + 1
            fout.write(str(int(n)))


def plotres(subdir_name):
    tmp_values_arr = []
    tmp_step_arr = []
    f_txts = glob.glob(f"{DIRNAME}/{subdir_name}/*.txt")
    for f_test in f_txts:
        with open(f_test, 'r') as tfile:
            for line in tfile:
                for step, element in enumerate(line.split(', ')):
                    tmp_values_arr.append(int(element))
                    tmp_step_arr.append(step)
        plt.plot(tmp_step_arr, tmp_values_arr)
        tmp_values_arr = []
        tmp_step_arr = []

    plt.xlabel('step number')
    plt.ylabel('value')
    plt.grid(True)
    plt.show()


def create_dir():
    if not os.path.exists(DIRNAME):
        os.mkdir(DIRNAME)
    date = datetime.datetime.now()
    subdir_name = str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '_' + str(date.hour) + '_' +\
               str(date.minute) + '_' + str(date.second)
    if not os.path.exists(f'{DIRNAME}/{subdir_name}'):
        os.mkdir(f'{DIRNAME}/{subdir_name}')

    return subdir_name


def create_threads(value, subdir_name):
    threads_pool = {}

    if value > THREAD_MAX_NUM:
        delta = value / THREAD_MAX_NUM
        for thread_num in range(THREAD_MAX_NUM):
            deltanum = THREADS_ARGS[thread_num] * delta
            threads_pool[thread_num] = Th(target=collatz_num, args=(value + deltanum, subdir_name,))
    else:
        thread_num = 0
        while value > 0:
            threads_pool[thread_num] = Th(target=collatz_num, args=(value, subdir_name,))
            thread_num += 1
            value -= 1

    return threads_pool


if __name__ == "__main__":
    to_continue = True

    while to_continue:
        value = 0
        found = False
        while not found:
            try:
               value = int(input("Insert any integer number greater than 1 :\n"))
               if value <= 1:
                    print("Invalid Value\n")
               else:
                    found = True
            except ValueError:
                print("Invalid Value\n")

        subdir_name = create_dir()
        threads_pool = create_threads(value, subdir_name)

        for thread in threads_pool.keys():
            threads_pool[thread].start()
        for thread in threads_pool.keys():
            threads_pool[thread].join()

        if not MULTIPLOT:
            plotres(subdir_name)
        else:
            plotres(subdir_name) #NOT ACTUALLY IMPLEMENTED
            #p = Process(target=plotres, args=(subdir_name,))
            #p.start()

        while True:
            try:
                to_continue = PROGRAM_STATE[int(input("Do you want to try another value?: 1-Yes 2-No\n"))]
                break
            except KeyError:
                print("Invalid Value\n")
            except ValueError:
                print("Invalid Value, not a number\n")
