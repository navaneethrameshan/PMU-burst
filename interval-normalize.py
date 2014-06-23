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

burst = True

if len(sys.argv) > 1:
    inf = open(sys.argv[1], "r")
else:
    inf = sys.stdin

printed_header = False
timestamp = None


if burst:
    file_out_name = sys.argv[1]+'-csv.csv'
else:
    file_out_name = sys.argv[1][:-4]+'-csv.csv'



if os.path.exists(file_out_name):
    os.remove(file_out_name)

if burst:
    output = open(sys.argv[1]+'-csv.csv','w+')

else:
    output = open(sys.argv[1][:-4]+'-csv.csv','w+')

events = dict()
rc = csv.reader(inf)
count = 0
ev = None
for row in rc:
    if burst:
        if len(row) == 2:
            count+=1
            val, ev = row
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
                print ",".join( events.keys())
                output.write(",".join( events.keys()))
                output.write("\n")
                printed_header = True
            print ",".join(map(lambda x: events[x], events.keys()))
            output.write( ",".join(map(lambda x: events[x], events.keys())))
            output.write("\n")
            events = dict()
            count=0

    events[ev] = val

output.close()

