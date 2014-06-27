import os
import config
import deploy
from fabric.tasks import execute


def get_execution_times():
    colocated_exec ={}
    estimated_exec={}

    execute(deploy.fetch_result,dir=config.execution_time_dir,hosts=["10.0.3.27","10.0.3.35"])

    files = os.listdir(config.execution_time_dir)
    #print files

    for file in files:
        f_handle= open(config.execution_time_dir+'/'+file,'r')
        processes = file.split('-') #[result or estimateddrop,process1,process2]
        source = processes[1]
        process_2 = processes[2].split('.')[0]

        for line in f_handle.readlines():
            content= line

        if processes[0] == "result":
            content = content.split()
            #FORMAT: content = ['runspec', 'finished', 'at', 'Thu', 'Jun', '26', '23:58:25', '2014;', '410', 'total', 'seconds', 'elapsed']
            exec_time= content[-4]
            try:
                if colocated_exec.has_key(source):
                    colocated_exec[source].update({process_2:float(exec_time)})
                else:
                    colocated_exec.update({source:{process_2:float(exec_time)}})
            except:
                continue
        else:
            exec_time= content
            try:
                if estimated_exec.has_key(source):
                    estimated_exec[source].update({process_2:float(exec_time)})
                else:
                    estimated_exec.update({source:{process_2:float(exec_time)}})
            except:
                continue



    print custom_sort('lbm',colocated_exec)
    print custom_sort('lbm',estimated_exec)

    return colocated_exec

def custom_sort(key, exec_dict):
    # Returns list of tuples sorted by value
    return sorted(exec_dict[key].items(),key= lambda x: x[1])

if __name__ == '__main__':

    get_execution_times()