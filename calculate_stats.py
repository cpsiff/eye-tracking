import json
import csv
import os

for subdir, dirs, files in os.walk('results'):
    for file in files:
        if file == 'gaze_converted.json':

            with open(os.path.join(subdir,'saccades.csv'), 'w+', newline='') as saccadesCSV:
                with open(os.path.join(subdir,'fixations.csv'),'w+', newline='') as fixationsCSV:

                    saccadesCSVWriter = csv.writer(saccadesCSV)
                    fixationsCSVWriter = csv.writer(fixationsCSV)
                    try:
                        with open(os.path.join(subdir,'movements.json')) as f:
                            data = json.loads(f.read())
                            fixationCount = 0
                        saccadeCount = 0
                        fixationDuration = 0
                        saccadeDuration = 0
                        for sample in data:
                            if sample['MovementType'] == 'Fixation':
                                fixationsCSVWriter.writerow([sample['MovementType'], int(sample['EndTimestamp']) - int(sample['Timestamp'])])
                                fixationCount += 1
                                fixationDuration += int(sample['EndTimestamp']) - int(sample['Timestamp'])
                            elif sample['MovementType'] == 'Saccade':
                                saccadesCSVWriter.writerow([sample['MovementType'], int(sample['EndTimestamp']) - int(sample['Timestamp'])])
                                saccadeCount += 1
                                saccadeDuration += int(sample['EndTimestamp']) - int(sample['Timestamp'])

                        with open(os.path.join(subdir,'stats.txt'), 'w+') as stats:
                            stats.write('# of Fixations: ' + str(fixationCount) + '\n')
                            stats.write('avg Fixation Duration: ' + str(fixationDuration/fixationCount) + '\n')
                            stats.write('# of Saccades: ' + str(saccadeCount) + '\n')
                            stats.write('avg Saccade Duration: ' + str(saccadeDuration/saccadeCount) + '\n')
                    except:
                        print('issue with', subdir, file)

                    
