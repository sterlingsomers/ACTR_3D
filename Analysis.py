__author__ = 'sterling'
import pickle





import glob, os
data = {}
#os.chdir('\home\sterling\Dropbox\SWAT%20research\Thesis\Data')
for root, dirs, files in os.walk('/home/sterling/Dropbox/SWAT research/Thesis/Data/small'):
    for dir in dirs:

        multiplier = float(dir[-4:-1])
        data[multiplier] = []
        datum = dict()
        for root2, dirs2, files2 in os.walk(os.path.join(root,dir)):

            for file2 in files2:

                with open(os.path.join(root,dir,file2)) as f:
                    for line in f:
                        if 'angle' in line:
                            datum['angle'] = float(line[6:])
                            #print(float(line[6:]))
                        if 'collision' in line:
                            try:
                                datum['collision'] = int(line[10:])
                            except ValueError:
                                datum['collision'] = 0
                data[multiplier].append(datum)
with open('small.pkl', 'wb') as f:
    pickle.dump(data,f)


