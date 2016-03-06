import os
import numpy as np

angles = []
for root, dirs, files in os.walk('./'):
    for fname in files:
        if 'average' in fname:
            continue
        with open(fname, "r") as f:
            
            for line in f:
                if 'angle' in line:
                    angles.append(float(line[6:-1]))
print(np.average(angles))
                    
