import os
import mainburst
import collections
from config import *

def process():


    list_dictionary = {} #{cpu-burst:{1:content,2:content,..},  mbw-burst:{1:content,..} }

    for key, values in map_pid_filename.items():
        list_dictionary[values['filename']] = {}
        for filename in os.listdir(csv_dir):
            name,numbercsv = filename.split("_")
            number,csv = numbercsv.split(".")

            if name == values['filename']:
                list_dictionary[values['filename']].update({int(number):open (csv_dir+filename, 'r')})


    # Now sort the numbers in list_dictionary

    #for key, value in list_dictionary.items():
    #    ordered_values = collections.OrderedDict(sorted(value.items()))
    #    list_dictionary[key] = ordered_values


    for key, values in list_dictionary.items():
        f= open (csv_dir+key, 'w')
        for number in sorted(values):
            print number
            f.writelines(values[number].readlines())

        f.close()

if __name__ =='__main__':
    process()


