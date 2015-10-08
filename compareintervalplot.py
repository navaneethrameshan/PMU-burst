#!/usr/bin/python
# plot interval CSV output from perf/toplev
# perf stat -I1000 -x, -o file ...
# toplev -I1000 -x, -o file ...
# intervalplotcompare.py file (or stdin)
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
import config

csv_file_handle = {}
value = dict()

def plot(files,  pstyle = 'ggplot', output=None, seq=None, xkcd=False):
    global csv_file_handle
    global value
    csv_file_handle ={}

    # op_sum = {'1':['L1-dcache-loads','L1-dcache-stores','L1-dcache-prefetches','L1-icache-loads'],
    #           '2':['L1-dcache-load-misses','L1-dcache-store-misses','L1-dcache-prefetch-misses','L1-icache-load-misses'],
    #           '3':[ 'LLC-loads','LLC-stores','LLC-prefetches'],
    #           '4':['LLC-load-misses','LLC-store-misses','LLC-prefetch-misses'],
    #           '5':['dTLB-loads','dTLB-stores','iTLB-loads'],
    #           '6':['dTLB-load-misses','dTLB-store-misses','iTLB-load-misses'],
    #           'Bandwidth':['offcore_response_corewb_local_dram_0','offcore_response_prefetch_any_llc_miss_0','LLC-prefetches','cache-misses']}
    #
    # op_div = [['cache-references','uops_retired_any'],['cache-misses','uops_retired_any'], ['instructions','cycles'],
    #           ['cache-misses','cache-references']]

    #enable for i7

    op_sum = {
        'contention': ['cache-misses'],
        'band': ['cache-references', 'cache-misses'],
        'total_bandwidth': ['cache-references'],
    }

    op_diff ={}

    op_div= [['cache-references','uops_retired_any'],['cache-misses','uops_retired_any'],
             ['instructions','cycles'],['cache-misses','cache-references'],['cache-references','cycles'], ['cache-misses','cycles']]

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
    assigned = dict() # assigned= {'mbw-cache-references': [0,2345,..], 'soplex-cache-references': [32,532,12,..], ..} Events and values for all processes

    if len(files) < 2 :
        print "More than one file needed. Exiting!"
        sys.exit(0)

    for file in files:
        processname = file.split("/")[-1]
        if  file:
            try:
                inf = open( file, "r")
            except:
                return
        else:
            inf = sys.stdin

        csv_file_handle[processname] = csv.reader(inf)

    timestamps = dict()

    val = ""
    first_time = True
    event_list = [] # event_list= [cache-references, instructions,..]

    for processname,rc in  csv_file_handle.items():

        for r in rc:
            if config.burst:
                if len(r) == 2:
                    ts=0
                    val, event = r
                    if  first_time and event not in event_list:
                        event_list.append(event)

                    event = str(processname)+"-"+event
                else:
                    continue

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

        first_time = False


    levels = dict()
    for j in assigned.keys():
        levels[gen_level.get_level(j)] = True

    if xkcd:
        try:
            plt.xkcd()
        except NameError:
            print "Please update matplotlib. Cannot enable xkcd mode."

    #print value

    if config.normalize:
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
    print "Assigned Keys: ", assigned.keys()
    #print "event list: ", event_list

    for l in levels.keys():
        ax = plt.subplot(len(levels), 1, n)
        if val.find('%') >= 0:
            ax.set_ylim(0, 100)
        t = []
        for j in event_list:
            print j, gen_level.get_level(j), l

            for processname in csv_file_handle:
                if gen_level.get_level(j) == l:
                    t.append(j)
                    ax.plot(value[str(processname)+"-"+j], label = str(processname)+"-"+j )

                if seq:
                    leg = ax.legend( loc='upper left')
                    leg.get_frame().set_alpha(0.5)
            plt.savefig(seq+"/"+j)
            plt.cla()

        leg = ax.legend(t, loc='upper left')
        leg.get_frame().set_alpha(0.5)
        n += 1

    if len(op_diff) > 0:
        for key, components in op_diff.items():
            print components
            #print [(value[component]) for component in components]
            #print [len(value[component]) for component in components]
            diff_value={}
            if key =='contention' :
                    print "KEY: ", key
                    ax1 = plt.subplot(2,1,1)
                    ax2 = plt.subplot(2,1,2)
            else:
                    ax = plt.subplot(1, 1, 1)

            for processname in csv_file_handle:

                diff_value[processname]=[x-y for x,y in zip(value[str(processname)+"-"+components[0]],value[str(processname)+"-"+components[1]])]

                #print sum_value
                #print "DONE!!"
               # print len(sum_value)
               # print len(timestamps[components[0]])
                if key is not 'contention':
                    ax.plot(diff_value[processname], label = str(processname)+"-"+'-'.join(components))
                else:
                    ax1.plot(diff_value[processname], label = str(processname)+"-"+'-'.join(components))

                if seq:
                    if key is not 'contention':
                        leg = ax.legend(loc='upper left')
                        leg.get_frame().set_alpha(0.5)
                    else:
                        leg = ax1.legend(loc='upper left')
                        leg.get_frame().set_alpha(0.5)

            if key =='contention':
            #plot the drop in performance of each process:
                perf_drop = compute_contention(diff_value)
                for process, drop in perf_drop.items():
                    ax2.plot(drop, label="Drop in perf of "+str(process))

                    #change to a function later
                    avg_perf_drop = sum(drop)/len(drop)
                    f_handle= open(config.execution_time_dir+'/estimateddrop-'+process+'-'+
                                   ''.join([p if p is not process else '' for p,d in perf_drop.items()])+'.log','w+')
                    f_handle.write(str(avg_perf_drop))
                    f_handle.close()

                    leg=ax2.legend(loc= 'upper left')
                    leg.get_frame().set_alpha(0.5)


            plt.savefig(seq+"/"+'+'.join(components))
            plt.cla()



    if len(op_sum) > 0:
        for key, components in op_sum.items():
            print components
            #print [(value[component]) for component in components]
            #print [len(value[component]) for component in components]
            sum_value={}
            if key =='contention' :
                    print "KEY: ", key
                    ax1 = plt.subplot(2,1,1)
                    ax2 = plt.subplot(2,1,2)
            else:
                    ax = plt.subplot(1, 1, 1)

            for processname in csv_file_handle:

                sum_value[processname]=sum(map(numpy.array, [value[str(processname)+"-"+component] for component in components]))
                #print sum_value
                #print "DONE!!"
               # print len(sum_value)
               # print len(timestamps[components[0]])
                if key is not 'contention':
                    ax.plot(sum_value[processname], label = str(processname)+"-"+'+'.join(components))
                else:
                    ax1.plot(sum_value[processname], label = str(processname)+"-"+'+'.join(components))

                if seq:
                    if key is not 'contention':
                        leg = ax.legend(loc='upper left')
                        leg.get_frame().set_alpha(0.5)
                    else:
                        leg = ax1.legend(loc='upper left')
                        leg.get_frame().set_alpha(0.5)

            if key =='contention':
            #plot the drop in performance of each process:
                perf_drop = compute_contention(sum_value)
                #print perf_drop
                for process, drop in perf_drop.items():
                    ax2.plot(drop, label="Drop in perf of "+str(process))

                    #change to a function later
                    if len(drop)>0:
                        avg_perf_drop = sum(drop)/len(drop)
                        f_handle= open(config.execution_time_dir+'/estimateddrop-'+process+'-'+
                                       ''.join([p if p is not process else '' for p,d in perf_drop.items()])+'.log','w+')
                        f_handle.write(str(avg_perf_drop))
                        f_handle.close()

                    leg=ax2.legend(loc= 'upper left')
                    leg.get_frame().set_alpha(0.5)

            elif key =='total_bandwidth':
                plt.cla()
                ax = plt.subplot(1, 1, 1)
                total_bw = total_bandwidth(sum_value)
                ax.plot(total_bw['total'], label = 'Total Bandwidth')
                leg = ax.legend(loc='upper left')
                leg.get_frame().set_alpha(0.5)

            plt.savefig(seq+"/"+key+": "+'+'.join(components))
            plt.cla()

    if len(op_div) > 0:
        ax = plt.subplot(1, 1, 1)

        for components in op_div:
            print components
            for processname in csv_file_handle:
                ax.plot([numpy.float64(x)/y for x,y in zip(value[str(processname)+"-"+components[0]],value[str(processname)+"-"+components[1]])], label= str(processname)+"-"+'/'.join(components))

            if seq:
                leg = ax.legend( loc='upper left')
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



def compute_drop(all_bw):
    '''

    :param all_list:dictionary containing bandwidth usage of each process. ex: {'process1':[..], 'process2':[]}
    :return: returns a dictionary of estimated drop in performance of each application
    '''

    max_Bandwidth = 4.3*10**8

    drop_in_performance = {}

    for processname in csv_file_handle:
    #In each iteration, compute the drop in performance for processname
        percentage_share= {}

        for current_process,bw_usage_list in all_bw.items():
        # For processname, compute the percentage share of unused bandwidth by all other processes
            if current_process == processname:
                continue
            percentage_share[current_process] =  []

            for i in xrange(0, len(all_bw[processname])):
                if i< len(bw_usage_list):
                    percentage_share[current_process].append(bw_usage_list[i]/(max_Bandwidth - all_bw[processname][i]))
                #else:
                   # percentage_share[current_process].append(0)

        drop_in_performance[processname] = sum(map(numpy.array, [percentage_share[process] for process in percentage_share]))

    return drop_in_performance



def total_bandwidth(all_bw):
    bw_used = {}
    list_total_bw_used = []
    for processname in csv_file_handle:
        for i in xrange(0, len(all_bw[processname])):
            list_total_bw_used.append (sum([all_bw[remaining_process][i]
                                            if i< len(all_bw[remaining_process])
                                            else 0  for remaining_process in csv_file_handle]))
        break

    bw_used['total'] = list_total_bw_used
    return bw_used

def compute_contention(all_bw):
    '''

    :param all_list:dictionary containing bandwidth usage of each process. ex: {'process1':[..], 'process2':[]}
    :return: returns a dictionary of estimated drop in performance of each application
    '''

    max_Bandwidth = 9*10**8 #for a 5 second sampling

    increase_in_performance = {}

    no_of_corunners = len(csv_file_handle)

   # print "Co Runners: ", no_of_corunners
    pressure_experienced= {}

    for processname in csv_file_handle:
    #In each iteration, compute the drop in performance for processname

        pressure_experienced[processname] =  []

        for i in xrange(0, len(all_bw[processname])):
            current_no_of_corunners = no_of_corunners
            list_total_bw_used = [all_bw[remaining_process][i] if i< len(all_bw[remaining_process]) else 0  for remaining_process in csv_file_handle]

            for val in list_total_bw_used:
                if val == 0:
                    current_no_of_corunners -=1

            total_bw_used=sum(list_total_bw_used)

            bw_free = max_Bandwidth -total_bw_used
            normalized_total_intensity_of_pressure_in_bw= total_bw_used/max_Bandwidth
            normalized_intensity_of_my_bw_usage = all_bw[processname][i]/max_Bandwidth
            total_cache_misses = sum([value[str(remaining_process)+"-"+'cache-misses'][i] if i< len(value[str(remaining_process)+"-"+'cache-misses']) else 0  for remaining_process in csv_file_handle])
            normalized_cache_misses = total_cache_misses/max_Bandwidth

            if processname == 'memcached':
                pressure_experienced[processname].append( normalized_total_intensity_of_pressure_in_bw )
        #else:
               # percentage_share[current_process].append(0)
    #print pressure_experienced

    return pressure_experienced

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
        for key,values in config.map_pid_filename.items():
            print "Plot and Store: ", values['filename']
            filename = config.csv_dir+values['filename']
            result_folder = config.result_dir+values['filename']
            print result_folder
            plot(filename, seq=result_folder)

    else:
        plot(args.files, args.style, args.output, args.seq,  args.xkcd)

__author__ = 'navaneeth'
