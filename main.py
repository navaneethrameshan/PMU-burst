__author__ = 'navaneeth'
import ocperf
import subprocess
import util
from subprocess import PIPE
counters=['cache-references','cache-misses','branch-instructions','branch-misses','stalled-cycles-frontend',
          'stalled-cycles-backend','io_transactions','ref-cycles','page-faults','context-switches',
          'cpu-migrations','minor-faults','major-faults','arith.cycles_div_busy','cache_lock_cycles.l1d',
          'cache_lock_cycles.l1d_l2','fp_comp_ops_exe.x87','ild_stall.any','ild_stall.iq_full','inst_queue_writes',
          'inst_retired.any','L1-dcache-loads','L1-dcache-stores','L1-dcache-prefetches','L1-icache-loads',
          'L1-dcache-load-misses','L1-dcache-store-misses','L1-dcache-prefetch-misses','L1-icache-load-misses',
          'LLC-loads','LLC-stores','LLC-prefetches', 'LLC-load-misses','LLC-store-misses','LLC-prefetch-misses',
          'dTLB-loads','dTLB-stores','iTLB-loads','dTLB-load-misses','dTLB-store-misses','iTLB-load-misses',
          'arith.div','arith.mul','uops_retired.any','resource_stalls.any','resource_stalls.fpcw','resource_stalls.load',
          'resource_stalls.mxcsr','resource_stalls.other','resource_stalls.rob_full','resource_stalls.rs_full',
          'resource_stalls.store','offcore_response.prefetch.local_dram_0','offcore_response.prefetch.local_dram_1',
          'offcore_response.prefetch.any_location_0','offcore_response.prefetch.any_location_1',
          'offcore_response.any_request.any_location_0','offcore_response.any_request.any_location_1',
          'br_inst_exec.cond','instructions','cycles','offcore_requests.any',
          'offcore_response.prefetch.any_llc_miss_0','offcore_response.prefetch.any_llc_miss_1',
          'offcore_response.corewb.local_dram_0','offcore_response.corewb.local_dram_1']

if __name__ == '__main__':
    pid = util.get_pid("mbw")
    print "PID: ", pid
    vm_1= subprocess.call(["python", "ocperf.py", "stat", "-e", ','.join(counters),"-I2000", "-x,", "-o", "mbw-cpu.csv", "-p",
                      pid], stdout=PIPE)
