# counters=['cache-references','cache-misses','branch-instructions','branch-misses','stalled-cycles-frontend',
#           'stalled-cycles-backend','io_transactions','ref-cycles','page-faults','context-switches',
#           'cpu-migrations','minor-faults','major-faults','arith.cycles_div_busy','cache_lock_cycles.l1d',
#           'cache_lock_cycles.l1d_l2','fp_comp_ops_exe.x87','ild_stall.any','ild_stall.iq_full','inst_queue_writes',
#           'inst_retired.any','L1-dcache-loads','L1-dcache-stores','L1-dcache-prefetches','L1-icache-loads',
#           'L1-dcache-load-misses','L1-dcache-store-misses','L1-dcache-prefetch-misses','L1-icache-load-misses',
#           'LLC-loads','LLC-stores','LLC-prefetches', 'LLC-load-misses','LLC-store-misses','LLC-prefetch-misses',
#           'dTLB-loads','dTLB-stores','iTLB-loads','dTLB-load-misses','dTLB-store-misses','iTLB-load-misses',
#           'arith.div','arith.mul','uops_retired.any','resource_stalls.any','resource_stalls.fpcw','resource_stalls.load',
#           'resource_stalls.mxcsr','resource_stalls.other','resource_stalls.rob_full','resource_stalls.rs_full',
#           'resource_stalls.store','offcore_response.prefetch.local_dram_0','offcore_response.prefetch.local_dram_1',
#           'offcore_response.prefetch.any_location_0','offcore_response.prefetch.any_location_1',
#           'offcore_response.any_request.any_location_0','offcore_response.any_request.any_location_1',
#           'br_inst_exec.cond','instructions','cycles','offcore_requests.any',
#           'offcore_response.prefetch.any_llc_miss_0','offcore_response.prefetch.any_llc_miss_1',
#           'offcore_response.corewb.local_dram_0','offcore_response.corewb.local_dram_1']


#for intelxeon
counters=['cache-references','cache-misses','instructions','cycles','stalled-cycles-frontend','arith.fpu_div','fp_comp_ops_exe.sse_packed_single','fp_comp_ops_exe.sse_scalar_double','fp_comp_ops_exe.sse_scalar_single','dtlb_load_misses.miss_causes_a_walk','inst_retired.any_p','mem_trans_retired.load_latency_gt_32','mem_uops_retired.all_loads','mem_uops_retired.all_stores','resource_stalls.any','resource_stalls.lb_sb','resource_stalls.mem_rs','resource_stalls.ooo_rsrc','dtlb_load_misses.walk_completed','dtlb_load_misses.walk_duration','dtlb_store_misses.walk_completed','dtlb_store_misses.walk_duration','itlb_misses.walk_completed','itlb_misses.walk_duration','cpu_clk_unhalted.thread_p','l2_lines_in.all']


monitor_period = 5
csv_dir = "csv-automated-burst-all/test/"
map_pid_filename = {'instance-000026af -uuid': {'filename':'memcached', 'type':'none'}, 'stream.out': {'filename':'stream', 'type':'affinity'}}

#for applications of 'type':'affinity' where applications are monitored based on the cores they run on instead of pid
cores = "4-7"
execution_time_dir="execution-times"

#### plot ###############################################
normalize= False
burst = True
result_dir = "result-automated-burst-all/test/"
