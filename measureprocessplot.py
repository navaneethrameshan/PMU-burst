import signal,sys
import mainburst,postprocess,intervalplot,compareintervalplot
import config
import argparse

csvdirname = None
resultdirname = None

def signal_handler(signal,frame):
    print "You pressed Ctrl+C"
    print "Post processing"
    postprocess.process(csvdirname)

    for key,values in config.map_pid_filename.items():
        print "Plot and Store: ", values['filename']
        filename = csvdirname+values['filename']
        result_folder = resultdirname+values['filename']
        intervalplot.plot(filename, seq=result_folder)

    files = [csvdirname+values['filename'] for key,values in config.map_pid_filename.items() ]
    compareintervalplot.plot(files, seq = resultdirname+'compare')


    print "Results can be found in: " + csvdirname
    sys.exit(0)

def process_plot():
    print "Post processing"
    postprocess.process(csvdirname)

    for key,values in config.map_pid_filename.items():
        print "Plot and Store: ", values['filename']
        filename = csvdirname+values['filename']
        print filename
        result_folder = resultdirname+values['filename']
        intervalplot.plot(filename, seq=result_folder)

    files = [csvdirname+values['filename'] for key,values in config.map_pid_filename.items() ]
    compareintervalplot.plot(files, seq = resultdirname+'compare')

    print "Results can be found in: " + csvdirname

def measure_process_plot():
    mainburst.measure(csvdirname)
    process_plot()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('-cd','--csvdir', action = "store", dest = 'csvdir', help = "Use this argument to generate folder name for CSV. Example: csv/" )
    parser.add_argument('-rd','--resultdir', action = "store", dest = 'resultdir', help = "Use this argument to generate folder name for Results. Example: Results/" )
    args = vars(parser.parse_args())


    if args['csvdir']:
        csvdirname = args['csvdir']
    else:
        csvdirname = config.csv_dir

    if args['resultdir']:
        resultdirname = args['resultdir']
    else:
        resultdirname = config.result_dir

    mainburst.measure(csvdirname)
    process_plot()
    print "Return SUCESS!!!!!!!!"