#!/usr/bin/python
# convert perf stat -Ixxx -x, / toplev -Ixxx -x, output to normalized output
# t1,ev1,num1
# t1,ev2,num1
# t2,ev1,num3
# ->
# timestamp,ev1,ev2
# t1,num1,num2
# t2,num3,,
import sys
import csv
import os
import config
import time


def interval_normalize(csvfile, burst = True):

    inf = open(csvfile, "r")

    printed_header = False
    timestamp = None


    if burst:
        file_out_name = csvfile+'-csv.csv'
    else:
        file_out_name = csvfile[:-4]+'-csv.csv'



    if os.path.exists(file_out_name):
        os.remove(file_out_name)

    if burst:
        output = open(csvfile+'-csv.csv','w+')

    else:
        output = open(csvfile[:-4]+'-csv.csv','w+')

    events = dict()
    rc = csv.reader(inf)
    count = 0
    ev = None
    for row in rc:
        if burst:
            if len(row) == 3:
                count+=1
                val,unit,ev = row
            elif len(row) == 2:
                count+=1
                val,ev = row
            else:
                continue

        else:
            if len(row) < 3:
                continue
            if len(row) > 3:
                ts, val, unit, ev = row
            else:
                ts, val, ev = row

        ev = ev.strip()

        if not burst:
            if ts != timestamp:
                if timestamp:
                    if not printed_header:
                        print ",".join(["Timestamp"] + events.keys())
                        output.write(",".join(["Timestamp"] + events.keys()))
                        output.write("\n")
                        printed_header = True
                    print timestamp + "," + ",".join(map(lambda x: events[x], events.keys()))
                    output.write(timestamp + "," + ",".join(map(lambda x: events[x], events.keys())))
                    output.write("\n")
                    events = dict()
                timestamp = ts
        else:
            if count > len(config.counters):
                if not printed_header:
                    print ",".join( sorted(events.keys()))
                    output.write(",".join( sorted(events.keys())))
                    output.write("\n")
                    printed_header = True
                print ",".join(map(lambda x: events[x], sorted(events.keys())))
                output.write( ",".join(map(lambda x: events[x], sorted(events.keys()))))
                output.write("\n")
                events = dict()
                count=1

        events[ev] = val
    output.close()

if __name__ == '__main__':
    interval_normalize('csv-command/memcached')