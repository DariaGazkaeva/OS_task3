#!/bin/python3

import os
import sys
import signal


produced = 0
pid1 = -1
pid2 = -1


def main():
    global produced
    global pid1
    global pid2

    pipe_read_1_0, pipe_write_1_0 = os.pipe()
    pipe_read_0_2, pipe_write_0_2 = os.pipe()
    pipe_read_2_0, pipe_write_2_0 = os.pipe()

    pid1 = os.fork()
    if pid1 != 0:
        pid2 = os.fork()
        if pid2 != 0:
            signal.signal(signal.SIGUSR1, on_signal)

            os.close(pipe_write_2_0)
            os.close(pipe_write_1_0)
            os.close(pipe_read_0_2)

            file1 = os.fdopen(pipe_read_1_0)
            file2 = os.fdopen(pipe_read_2_0)
            file3 = os.fdopen(pipe_write_0_2, "w")

            while True:
                line = file1.readline()
                if not line:
                    break
                file3.write(line)
                file3.flush()
                res = file2.readline()
                print(line[:-1], "=", res[:-1])
                produced += 1

            file1.close()
            file2.close()
            file3.close()
        else:
            os.dup2(pipe_read_0_2, 0)
            os.dup2(pipe_write_2_0, 1)

            os.close(pipe_read_1_0)
            os.close(pipe_write_1_0)
            os.close(pipe_write_0_2)
            os.close(pipe_read_2_0)

            os.execl("/usr/bin/bc", "bc")
    else:
        os.dup2(pipe_write_1_0, 1)

        os.execl("./producer.py", "producer.py")

        os.close(pipe_read_2_0)
        os.close(pipe_write_2_0)
        os.close(pipe_read_0_2)
        os.close(pipe_write_0_2)
        os.close(pipe_read_1_0)


def on_signal(signal_number, stack_frame):
    print("Produced:", produced, file=sys.stderr)
    os.kill(pid1, signal_number)
    os.kill(pid2, signal_number)
    exit()


main()
