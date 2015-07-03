from pi_est import MontecarloPi


# How to run this:
# Generally you would run this with (MRJob instllaed):
# python mr-pi-driver.py  

# To tun this locally, use the following line where input.txt is the input
# file.  
mr_job=MontecarloPi(args=['-r', 'local', 'input.txt'])
# To run on emr, uncomment the followign line and comment the above line.
#mr_job=MontecarloPi(args=['-r', 'emr', 'input_pi.txt'])
with mr_job.make_runner() as runner:
     runner.run()
     monte_counts = [mr_job.parse_output_line(line) for line in
            runner.stream_output()]
     nhits_tuple= monte_counts[0]
     ntrials_tuple= monte_counts[1]
     ntrials_tot= ntrials_tuple[1]
     nhits_tot= nhits_tuple[1]
     print "n_trials= ",ntrials_tot
     print "n_hits= ",nhits_tot
     print "pi= ", 4.0*float(nhits_tot)/ntrials_tot
