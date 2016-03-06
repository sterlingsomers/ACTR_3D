import os
import numpy as np

angles = []
collisions = []
for root, dirs, files in os.walk('./'):
    for fname in files:
        if 'average' in fname:
            continue
        with open(fname, "r") as f:
            
            for line in f:
                if 'angle' in line:
                    angles.append(float(line[6:-1]))
                if 'collision' in line:
                    try:
                        collisions.append(int(line[10:-1]))
                    except ValueError:
                        collisions.append(0)

print("Angles:",sorted(angles))
print("Average Angles:", np.average(angles))

print("Collisions", collisions)
print("Avg. Collisions:", np.average(collisions))
print(len(angles))
                    
