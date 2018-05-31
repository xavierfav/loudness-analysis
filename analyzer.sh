#!/bin/bash

#SBATCH -J analyzer
#SBATCH -p high
#SBATCH --workdir=/homedtic/xfavory/dev/loudness-analysis/
#SBATCH --array=1-400:1
#SBATCH --ntasks=1


#SBATCH -o /homedtic/xfavory/dev/loudness-analysis/out/%J.%u.%a.out # STDOUT
#SBATCH -e /homedtic/xfavory/dev/loudness-analysis/out/%J.%u.%a.err # STDERR

printf "[----]\n"
printf "Starting execution of job $SLURM_JOB_ID from user $LOGNAME\n"
printf "Starting at `date`\n"
start=`date +%s`

python analyzer.py ${SLURM_ARRAY_TASK_ID}

end=`date +%s`

printf "\n[----]\n"
printf "Job done. Ending at `date`\n"
runtime=$((end-start))
printf "It took: $runtime sec.\n"

