import signal,sys
import mainburst,postprocess,intervalplot,compareintervalplot
import config

def signal_handler(signal,frame):
    print "You pressed Ctrl+C"
    print "Post processing"
    postprocess.process()

    for key,values in config.map_pid_filename.items():
        print "Plot and Store: ", values['filename']
        filename = config.csv_dir+values['filename']
        result_folder = config.result_dir+values['filename']
        intervalplot.plot(filename, seq=result_folder)

    files = [config.csv_dir+values['filename'] for key,values in config.map_pid_filename.items() ]
    compareintervalplot.plot(files, seq = config.result_dir+'compare')


    print "Results can be found in: " + config.csv_dir


def process_plot():
   # print "Post processing"
   # postprocess.process()

    for key,values in config.map_pid_filename.items():
        print "Plot and Store: ", values['filename']
        filename = config.csv_dir+values['filename']
        result_folder = config.result_dir+values['filename']
        intervalplot.plot(filename, seq=result_folder)

    files = [config.csv_dir+values['filename'] for key,values in config.map_pid_filename.items() ]
    compareintervalplot.plot(files, seq = config.result_dir+'compare')

    print "Results can be found in: " + config.csv_dir

def measure_process_plot():
    #mainburst.measure()
    process_plot()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    mainburst.measure()
    process_plot()
    print "Return SUCESS!!!!!!!!"