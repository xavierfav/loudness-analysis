import sys
import os
import subprocess
import json
import time
from datetime import datetime
import progress_bar
import tempfile

OUTPUT_DIR = "./analysis/"
CMD_DIR = "/usr/local/bin/"
COMMAND = "essentia_streaming_extractor_music {} {}"

DEVNULL = open('/dev/null', 'wb')

def log(s):
    sys.stdout.write("[ {} ]\t".format(
        datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
    )
    sys.stdout.write(str(s) + "\n")
    sys.stdout.flush()

def extract(list_filenames, job_id):
    output_dict = dict()
    files_not_analyzed = list()
    pb = progress_bar.ProgressBar(len(list_filenames), 30, 'Analyzing audio files')

    # Log stuff
    log("Job started on {}".format(
        time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    ))
    log("Batch number {}".format(job_id))
    start = time.time()        
    pb.update(0)

    for index, audiofile in enumerate(list_filenames):        
        # Path to audiofile:
        #       sounds/<FOLDER NUMBER>/<FS SOUND ID>_<FS USER ID>.<EXTENSION>
        filename = audiofile.split("/")[-1]
        fs_id = filename.split("_")[0]

        #log("Analyzing file {}".format(filename))
        
        output_dict[fs_id] = dict()
        tmp = tempfile.NamedTemporaryFile()
        cmd = CMD_DIR + COMMAND.format(audiofile, tmp.name)
        try:
            # call Essentia's MusicExtractor
            process = subprocess.Popen(cmd.split(), stdout=DEVNULL, stderr=DEVNULL)
            process.communicate()
            # load computed descriptors
            data = json.load(tmp)
            output_dict[fs_id]["ebur128"] = data["lowlevel"]["loudness_ebu128"]["integrated"]
            output_dict[fs_id]["replayGain"] = data["metadata"]["audio_properties"]["replay_gain"]
            #log("{} analyzed succesfully".format(filename))
        except Exception as e:
            log("A problem occurred while analyzing {}".format(filename))
            log(e)
            files_not_analyzed.append(fs_id)
            output_dict[fs_id]["ebur128"] = None
            output_dict[fs_id]["replayGain"] = None
        tmp.close()
        pb.update(index+1)

    time_passed = time.time() - start
    out_filename = "{}{}.json".format(OUTPUT_DIR, job_id)

    try:
        if not os.path.exists(OUTPUT_DIR):
            #log("Warning: output folder '{}' doesn't exist. I'm creating it...".format(OUTPUT_DIR))
            os.makedirs(OUTPUT_DIR)
            #log("Output folder created successfully.")
        #log("Writing output file to '{}'...".format(out_filename))
        with open(out_filename, 'w') as output_file:
            json.dump(output_dict, output_file)
            #log("Output file succesfully written.")
    except Exception as e:
        log("Failed to write output file to {}.".format(out_filename))
        log(e)
    
    # Log additional information
    sys.stdout.write("\n")
    sys.stdout.flush()
    log("Files not analyzed: {}".format(len(files_not_analyzed)))
    log("Execution time: {} seconds.".format(time_passed))

if __name__ == "__main__":
    files = ["095_456.mp3", "123_123.wav", "456_123.mp3", "789_456.mp3"]
    root = "sounds/0/"
    extract([root + f for f in files], 0)