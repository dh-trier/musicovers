import os
import os.path

# csv-dateien anlegen
for method in ['svm', 'neighbors', 'tree']:
    outfile = 'compare_data_{}.csv'.format(method)
    if os.path.isfile(outfile):
        os.remove(outfile)
    outstr = 'n;mean_accuracy;std_of_accuracy;kern_or_neighbors;weights\n'
    with open(outfile, 'w') as sd:
        sd.write(outstr)

# für jeden Tree mit verschiedenen n's etc. ausführen
for i in range(2, 6):
    command = 'python3 7KL-001.py "{\'classifier\': \'tree\', \'n\':'  + str(i) + '}"'
    os.system(command)
    # für tree geht irgendwie nicht mehr

for kern in ['linear', 'poly', 'rbf']:
    for i in range(2, 5):
        command = 'python3 7KL-001.py "{\'classifier\': \'svm\', \'n\':'  + str(i) + ', \'svm_kernel\': \'{}\''.format(kern) +'}"'
        print(command)
        os.system(command)




    # command = 'python3 7KL-001.py "{\'classifier\':  ' + str(i) + '}"'
    # os.system(command)
# for i in range(10, 50, 5):
#     os.system('python3 7KL-001.py "{\'classifier\': \'tree\', \'n\': {0}}"'.format(i))
