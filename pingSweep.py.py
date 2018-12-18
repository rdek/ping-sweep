#!/usr/bin/env python

import multiprocessing
import subprocess
import sys
import os
import ipaddress
import locale

language, output_encoding = locale.getdefaultlocale()
def pinger( job_q, results_q):
    DEVNULL = open(os.devnull,'w')
    while True:
        ip = job_q.get()
        if ip is None: break

        try:
            subprocess.check_call(['ping','-c1',ip], stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

if __name__ == '__main__':
    if sys.argv[1] == 0:
        print "Skrypt przyjmuje arkument w postaci adresu IP!"
        exit 

    
    pool_size = 255

    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [ multiprocessing.Process(target=pinger, args=(jobs,results))
            for i in range(pool_size) ]

    for p in pool:
        p.start()
    
    ipaddr = sys.argv[1]
    ipaddr = ipaddr.decode('utf8')
    ipaddr = ipaddress.ip_address(ipaddr)
    for i in range(1,255):
        jobs.put(ipaddr.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    while not results.empty():
        ip = results.get()
        print(ip)
