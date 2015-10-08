#!/usr/bin/python
# plot interval CSV output from perf/toplev
# perf stat -I1000 -x, -o file ...
# toplev -I1000 -x, -o file ... 
# interval-plot.py file (or stdin)
# delimeter must be ,
# this is for data that is not normalized
# TODO: move legend somewhere else where it doesn't overlap?
from __future__ import division
import csv
import os
import sys
import matplotlib.pyplot as plt
import collections
import argparse
import shutil
import numpy
import time
from config import *



def plot(file,  pstyle = 'ggplot', output=None, seq=None, xkcd=False):

    # op_sum = {'1':['L1-dcache-loads','L1-dcache-stores','L1-dcache-prefetches','L1-icache-loads'],
    #           '2':['L1-dcache-load-misses','L1-dcache-store-misses','L1-dcache-prefetch-misses','L1-icache-load-misses'],
    #           '3':[ 'LLC-loads','LLC-stores','LLC-prefetches'],
    #           '4':['LLC-load-misses','LLC-store-misses','LLC-prefetch-misses'],
    #           '5':['dTLB-loads','dTLB-stores','iTLB-loads'],
    #           '6':['dTLB-load-misses','dTLB-store-misses','iTLB-load-misses'],
    #           'Bandwidth':['offcore_response_corewb_local_dram_0','offcore_response_prefetch_any_llc_miss_0','LLC-prefetches','cache-misses']}
   # op_div = [['cache-references','uops_retired_any'],['cache-misses','uops_retired_any'], ['instructions','cycles'],
   #           ['cache-misses','cache-references']]


    #enable for i7

    op_sum = {
        'contention': ['cache-misses'],
        'band': ['cache-references', 'cache-misses'],
        'total_bandwidth': ['cache-references']
    }

    op_div= [['instructions','cycles'],['cache-misses','cache-references'],['cache-references','cycles'], ['cache-misses','cycles']]


    print  pstyle
    if  pstyle:
        try:
            from mpltools import style
            style.use( pstyle)
        except ImportError:
            print "Need mpltools for setting  styles (pip install mpltools)"

    import gen_level

    try:
        import brewer2mpl
        all_colors = brewer2mpl.get_map('Paired', 'Qualitative', 12).hex_colors
    except ImportError:
        print "Install brewer2mpl for better colors (pip install brewer2mpl)"
        all_colors = ('green','orange','red','blue',
                  'black','olive','purple','#6960EC', '#F0FFFF',
                  '#728C00', '#827B60', '#F87217', '#E55451', # 16
                  '#F88017', '#C11B17', '#17BFC2', '#C48793') # 20

    cur_colors = collections.defaultdict(lambda: all_colors)
    assigned = dict()

    if  file:
        try:
            inf = open( file, "r")
        except:
            return
    else:
        inf = sys.stdin

    rc = csv.reader(inf)
    timestamps = dict()
    value = dict()

    val = ""
    for r in rc:
        if burst:
            if len(r) == 2:
                ts=0
                val, event = r
            else:
                continue

        if not burst:
            # timestamp,event,value
            if len(r) < 3:
                continue
            print r
            if len(r) >= 5:
                ts, event, val, thresh, desc = r
            elif len(r) >= 4:
                ts, val, unit, event = r
            else:
                ts, val, event = r


        if event not in assigned:
            level = gen_level.get_level(event)
            assigned[event] = cur_colors[level][0]
            cur_colors[level] = cur_colors[level][1:]
            if len(cur_colors[level]) == 0:
                cur_colors[level] = all_colors
            value[event] = []
            timestamps[event] = []
        timestamps[event].append(float(ts))
        try:
            value[event].append(float(val.replace("%","")))
        except ValueError:
            value[event].append(0.0)

    levels = dict()
    for j in assigned.keys():
        levels[gen_level.get_level(j)] = True

    if xkcd:
        try:
            plt.xkcd()
        except NameError:
            print "Please update matplotlib. Cannot enable xkcd mode."

    #print value

    if normalize:
        for key in value:
            entries= value[key]
            normalized_values = [numpy.float64(entry)/max(entries) for entry in entries]
            value[key] = normalized_values
    if seq:
        os.umask(0000)
        if os.path.exists(seq):
            shutil.rmtree(seq)
            os.makedirs(seq)
        else:
            os.makedirs(seq)


    n = 1
    print assigned.keys()
    for l in levels.keys():
        ax = plt.subplot(len(levels), 1, n)
        if val.find('%') >= 0:
            ax.set_ylim(0, 100)
        t = []
        for j in assigned.keys():
            print j, gen_level.get_level(j), l
            if gen_level.get_level(j) == l:
                t.append(j)
                if not burst:
                    if 'style' not in globals():
                        ax.plot(timestamps[j], value[j], assigned[j])
                    else:
                        ax.plot(timestamps[j], value[j])
                else:
                    ax.plot(value[j])

            if seq:
                leg = ax.legend([j], loc='upper left')
                leg.get_frame().set_alpha(0.5)
                plt.savefig(seq+"/"+j)
                plt.cla()

        leg = ax.legend(t, loc='upper left')
        leg.get_frame().set_alpha(0.5)
        n += 1


    if len(op_sum) > 0:
        for key, components in op_sum.items():
            print components
            #print [(value[component]) for component in components]
            #print [len(value[component]) for component in components]
            sum_value=sum(map(numpy.array, [value[component] for component in components]))
            #print sum_value
            #print "DONE!!"
           # print len(sum_value)
           # print len(timestamps[components[0]])
            if not burst:
                ax.plot(timestamps[components[0]], sum_value)
            else:
                ax.plot(sum_value)
            if seq:
                leg = ax.legend(['+'.join(components)], loc='upper left')
                leg.get_frame().set_alpha(0.5)
                plt.savefig(seq+"/"+'+'.join(components))
                plt.cla()

    if len(op_div) > 0:
        for components in op_div:
            print components
            if not burst:
                ax.plot(timestamps[components[0]],[numpy.float64(x)/y for x,y in zip(value[components[0]],value[components[1]])])
            else:
                ax.plot([numpy.float64(x)/y for x,y in zip(value[components[0]],value[components[1]])])

            if seq:
                leg = ax.legend(['/'.join(components)], loc='upper left')
                leg.get_frame().set_alpha(0.5)
                plt.savefig(seq+"/"+'_'.join(components))
                plt.cla()

    plt.xlabel('Time')
    if val.find('%') >= 0:
        plt.ylabel('Bottleneck %')
    else:
        plt.ylabel("Counter value")
    if output:
        plt.savefig(output)
    else:
        if not seq:
            plt.show()


if __name__ =='__main__':

    p = argparse.ArgumentParser(
            usage='plot interval CSV output from perf stat/toplev',
            description='''
    perf stat -I1000 -x, -o file ...
    toplev -I1000 -x, -o file ...
    intervalplot.py file (or stdin)
    delimeter must be ,
    this is for data that is not normalized.''')
    p.add_argument('--xkcd', action='store_true', help='enable xkcd mode')
    p.add_argument('--style', help='set mpltools style (e.g. ggplot)')
    p.add_argument('file', help='CSV file to plot (or stdin)', nargs='?')
    p.add_argument('--output', '-o', help='Output to file. Otherwise show.',
                   nargs='?')
    p.add_argument('--seq', help = 'Save the plots as individual images', nargs='?')
    p.add_argument('--auto', action='store_true', help='enable auto mode and plot from config files automatically')

    args = p.parse_args()
    #print args

    if args.auto:
        for key,values in map_pid_filename.items():
            print "Plot and Store: ", values['filename']
            filename = csv_dir+values['filename']
            result_folder = result_dir+values['filename']
            print result_folder
            plot(filename, seq=result_folder)

    else:
        plot(args.file, args.style, args.output, args.seq,  args.xkcd)

