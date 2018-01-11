import os
import os.path

print('\nErstelle Dateien...\n')

# csv-dateien anlegen
for method in ['svm', 'neighbors', 'tree']:
    outfile = 'compare_data_{}.csv'.format(method)
    if os.path.isfile(outfile):
        os.remove(outfile)
    if method == 'tree':
        outstr = 'n;mean_accuracy;std_of_accuracy;\n'
    elif method == 'svm':
        outstr = 'n;mean_accuracy;std_of_accuracy;kernel\n'
    elif method == 'neighbors':
        outstr = 'n;mean_accuracy;std_of_accuracy;k_neighbors;weights\n'

    with open(outfile, 'w') as sd:
        sd.write(outstr)


print('\nBenutze Decision Trees...\n')
# für jeden Tree mit verschiedenen n's etc. ausführen
for i in range(2, 10):
    command = 'python3 7KL-001.py "{\'classifier\': \'tree\', \'n\':'  + str(i) + '}"'
    print('\n' + command + '\n')
    os.system(command)
    # für tree geht irgendwie nicht mehr
    # vielleicht jetzt?


print('\nBenutze Support Vector Machines...\n')
# Für SVM mit verschiedenen Kernels ausprobieren
for kern in ['linear', 'poly', 'rbf']:
    for i in range(2, 10):
        command = 'python3 7KL-001.py "{\'classifier\': \'svm\', \'n\':'  + str(i) + ', \'svm_kernel\': \'{}\''.format(kern) +'}"'
        print('\n' + command + '\n')
        os.system(command)


print('\nBenutze K Nearest Neighbors...\n')
k_values = list(range(3, 10)) + list(range(10, 35, 5))
for n in range(2, 10): # Anzahl der Lern/Test-Teilungen
    for k in k_values: # Anzahl der k neighbors
        for weight in ['distance', 'uniform']:
            command = 'python3 7KL-001.py "{\'classifier\': \'neighbors\', \'n\':'  + str(n) + ', \'n_neighbors\': {}, \'weights\': \'{}\''.format(str(k), weight) +'}"'
            print('\n' + command + '\n')
            os.system(command)


