# Athanasios Athanassiadis Jan 2012
import numpy as np

# write the chain-code
def write_chain(fn, chain):
    with open(fn,'w') as of:
        for i in chain:
            of.write('{} '.format(i))
    print 'Successfully wrote: '+fn