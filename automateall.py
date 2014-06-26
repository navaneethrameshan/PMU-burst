import util
import measureprocessplot
import time
import deploy
from fabric.tasks import execute

spec_benchmarks= ['400.perlbench','437.leslie3d','462.libquantum','401.bzip2','444.namd','464.h264ref','403.gcc',
                  '445.gobmk','465.tonto','410.bwaves','470.lbm','416.gamess','450.soplex','471.omnetpp',
                  '453.povray','473.astar','433.milc','454.calculix','481.wrf','434.zeusmp','456.hmmer','435.gromacs',
                  '458.sjeng','483.xalancbmk','436.cactusADM','459.GemsFDTD','998.specrand']

single_application =True

if __name__ =='__main__':

    for i in xrange(0,len(spec_benchmarks)):
        for j in xrange(i+1, len(spec_benchmarks)):
            execute(deploy.run_spec,app=spec_benchmarks[i], result="result-"+spec_benchmarks[i][4:]+"-"+spec_benchmarks[j][4:]+".log",hosts=["10.0.3.27"])
            time.sleep(1)
            execute(deploy.run_spec,app=spec_benchmarks[j], result="result-"+spec_benchmarks[j][4:]+"-"+spec_benchmarks[i][4:]+".log",hosts=["10.0.3.35"])

            util.setup_config(spec_benchmarks[i],spec_benchmarks[j])
            time.sleep(4)
            measureprocessplot.measure_process_plot()