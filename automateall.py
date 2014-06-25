import util
import measureprocessplot
import time
import deploy
from fabric.tasks import execute

spec_benchmarks= ['471.omnetpp','470.lbm','450.soplex','453.povray','444.namd','458.sjeng']


if __name__ =='__main__':

    for i in xrange(0,len(spec_benchmarks)):
        for j in xrange(i+1, len(spec_benchmarks)):
            execute(deploy.run_spec,app=spec_benchmarks[i], result="result-"+spec_benchmarks[i][4:]+"-"+spec_benchmarks[j][4:]+".log",hosts=["10.0.3.27"])
            time.sleep(2)
            execute(deploy.run_spec,app=spec_benchmarks[j], result="result-"+spec_benchmarks[j][4:]+"-"+spec_benchmarks[i][4:]+".log",hosts=["10.0.3.35"])

            util.setup_config(spec_benchmarks[i],spec_benchmarks[j])
            time.sleep(4)
            measureprocessplot.measure_process_plot()