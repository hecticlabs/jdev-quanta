import time
from quantalib import qubits, processor

count = 12288
inp = qubits([x for x in range(count)], [1] * count)
print("Created Input")

proc = processor()
proc.compile("""
v = x ** e
w = wx
""")
print("Compiled Source")

print("Started processing")
start = time.time()
proc.run({
    'x': inp
}, { 'e': 2 })
end = time.time()
print("Finished processing")
print("Processing took " + str(round(end - start, 2)) + "s")

print("Measuring...")
outp = proc.measure()

print("Measured:")
print(outp)
