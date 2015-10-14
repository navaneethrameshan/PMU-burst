import os
import mainburst
import collections
import config
import intervalnormalize

def process(csvdir=None):

    csvdirname = config.csv_dir

    if csvdir:
        csvdirname = csvdir

    list_dictionary = {} #{cpu-burst:{1:content,2:content,..},  mbw-burst:{1:content,..} }

    for key, values in config.map_pid_filename.items():
        list_dictionary[values['filename']] = {}
        for filename in os.listdir(csvdirname):
            if "cpu" not in filename:
                name,numbercsv = filename.split("_")
                number,csv = numbercsv.split(".")
            else:
                continue

            if name == values['filename']:
                list_dictionary[values['filename']].update({int(number):open (csvdirname+filename, 'r')})


    # Now sort the numbers in list_dictionary

    #for key, value in list_dictionary.items():
    #    ordered_values = collections.OrderedDict(sorted(value.items()))
    #    list_dictionary[key] = ordered_values


    for key, values in list_dictionary.items():
        if len(values) >0 :
            name =csvdir+key
            f= open (name, 'w')
        for number in sorted(values):
            #print number
            f.writelines(values[number].readlines())

        try:
            f.close()
        except:
            continue
        #convert also to csv format for excel
        print "Converting to CSV"
        intervalnormalize.interval_normalize(name)




if __name__ =='__main__':
    process()


