import sys
from vcd import VCDWriter
with VCDWriter(sys.stdout, timescale='1 ns', date='today') as writer:
    counter_var = writer.register_var('a.b.c', 'counter', 'integer', size=8)
    for timestamp, value in enumerate(range(0, 32, 1)):
        writer.change(counter_var, timestamp, value)
