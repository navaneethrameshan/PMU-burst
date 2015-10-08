import signal,sys
import mainburst,postprocess,intervalplot,compareintervalplot
import config
import argparse

csvdirname = None
resultdirname = None
cores = None

def signal_handler(signal,frame):
    print "You pressed Ctrl+C"
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('-cd','--csvdir', action = "store", dest = 'csvdir', help = "Use this argument to generate folder name for CSV. Example: csv/" )
    parser.add_argument('-rd','--resultdir', action = "store", dest = 'resultdir', help = "Use this argument to generate folder name for Results. Example: Results/" )
    parser.add_argument('-cores','--cores', action = "store", dest = 'cores', help = "Use this argument to specify the cores perf needs to monitor applications of type:affinity. Example -cores 4-7" )
    args = vars(parser.parse_args())


    if args['csvdir']:
        csvdirname = args['csvdir']
    else:
        csvdirname = config.csv_dir

    if args['resultdir']:
        resultdirname = args['resultdir']
    else:
        resultdirname = config.result_dir

    if args['cores']:
        cores = args['cores']
    else:
        cores = config.cores

    mainburst.measure(csvdirname)
    print "Return SUCESS!!!!!!!!"