"""
kill_proc.py

kill a process by name
same effect as 'kill -9 <process id>' or 'pkill -9 <process name>'

Author: Yanan Zhao <ya_nanzhao@hotmail.com>
Date  : 2015-09-02
"""
import sys
import os
import subprocess

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python kill_proc.py <process name>")
        sys.exit(1)

    proc_name = sys.argv[1]
    print("killing process %s" % proc_name)

    p = subprocess.Popen(["ps", "-e"], stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, b''):
        tokens = line.decode('utf-8').strip().split()
        if proc_name in tokens:
            print("process found: %s" % proc_id)
            proc_id = tokens[0]

            print("kill process [%s: %s] ..." % (proc_id, proc_name))
            ret_code = subprocess.call(["kill", "-9", proc_id])
            if ret_code == 0:
                print(" successful")
            else:
                print(" failed")

            sys.exit(0)

    print("process %s not found" % proc_name)
