import sys
import json
import os
import math
from loudness_analyzer import extract

NUM_JOBS = 100
BASE_FOLDER = '/datasets/MTG/audio/incoming/freesound/sounds/'
FS_IDS = 'failed_ids.json'


def fs_id_to_folder(fs_id):
    return str(int(int(fs_id)/1000)) + '/'

def fs_id_to_filename(fs_id):
    folder = fs_id_to_folder(fs_id)
    filenames = os.listdir(BASE_FOLDER + folder)
    try:
        return folder + list(filter(lambda x: str(fs_id) + '_' in x, filenames))[0]
    except:
        return None
    

if __name__ == '__main__':
    fs_id_to_process = json.load(open(FS_IDS, 'rb'))
    num_files_per_job = int(math.ceil(len(fs_id_to_process)/float(NUM_JOBS)))

    # job id of this analyzer job
    job_id = int(sys.argv[1]) - 1
    filenames_to_process = [None]*num_files_per_job
    
    for idx, fs_id in enumerate(fs_id_to_process[job_id*num_files_per_job:(job_id+1)*num_files_per_job]):
        filenames_to_process[idx] = fs_id_to_filename(fs_id)

    filenames_to_process = [BASE_FOLDER + f for f in filenames_to_process if f]
    
    sys.stdout.write('\nSub filename list created:\n {0} \n'.format(filenames_to_process))
    sys.stdout.flush()

    extract(filenames_to_process, job_id)
