import os
import csv
name = ''
stats_blank = {'fnum':{'bionic':'', 'control':'', 'random':''},
        'snum':{'bionic':'', 'control':'', 'random':''},
        'flen':{'bionic':'', 'control':'', 'random':''},
        'slen':{'bionic':'', 'control':'', 'random':''},
        'normf':{'bionic':'', 'control':'', 'random':''},
        'norms':{'bionic':'', 'control':'', 'random':''},
        'duration':{'bionic':'', 'control':'', 'random':''},
        'normd':{'bionic':'', 'control':'', 'random':''}}
stats = stats_blank
with open('compiled_stats.csv','w+', newline='') as csvstats:
    csvwriter = csv.writer(csvstats)
    csvwriter.writerow(['Name', '', '# Fixations', '', '','# Saccades','', '','Avg Fixation Length','', '','Avg Saccade Length','', '', 'Normalized # Fixations','', '','Normalized # Saccades','', '','Duration','', '','Normalized Duration'])
    csvwriter.writerow(['','Bionic', 'Control', 'Random','Bionic', 'Control', 'Random','Bionic', 'Control', 'Random','Bionic', 'Control', 'Random','Bionic', 'Control', 'Random','Bionic', 'Control', 'Random','Bionic', 'Control', 'Random','Bionic', 'Control', 'Random'])
    for subdir, dirs, files in os.walk('results'):
        for file in files:
            if not 'example' in subdir:
                name_temp = subdir.split('/')[1].split('-')[2]
                if not name == name_temp:
                    if not name == '':
                        row = [name]
                        for key in stats:
                            for key2 in stats[key]:
                                row.append(str(stats[key][key2]).strip())
                        csvwriter.writerow(row)
                    name = name_temp
                    stats = stats_blank

                style = subdir.split('/')[2].split('_')[3]
                word_count = 0
                if subdir.split('/')[2].split('_')[2] == '1':
                    word_count = 412
                elif subdir.split('/')[2].split('_')[2] == '2':
                    word_count = 465
                elif subdir.split('/')[2].split('_')[2] == '3':
                    word_count = 562
                
                if file == 'stats.txt':
                    with open(os.path.join(subdir,file), 'r') as f:
                        stats['fnum'][style] = f.readline().split(':')[1]
                        stats['flen'][style] = f.readline().split(':')[1]
                        stats['snum'][style] = f.readline().split(':')[1]
                        stats['slen'][style] = f.readline().split(':')[1]

                        stats['normf'][style] = int(stats['fnum'][style]) / word_count 
                     
                        stats['norms'][style] = int(stats['snum'][style]) / word_count 
                 
                        
                if file == 'trial.yaml':
                    with open(os.path.join(subdir,file), 'r') as y:
                        stats['duration'][style] = y.readline().split(':')[1]
                        stats['normd'][style] = float(stats['duration'][style].replace('\n', '').strip())/word_count
                
                

            
