# loudness-analysis

This script is used to extract EBUR-128 and ReplayGain values from a list of audio files, using Essentia's MusicExtractor algorithm.

## Usage
To use it, launch the `analyzer.sh` shell script. Be sure to change the path to wherever your files are stored!
```shell
#SBATCH --workdir=/PATH/TO/AUDIO/FILES/
```
We provided some sample sounds in the `sounds/0/` folder.

## Notes
For now, the binary MusicExtractor (`essentia_streaming_extractor_music`) is not cross-platform, and is a non-standard modification of the original algorithm.

You can find the source code of this modified version here: https://github.com/lorenzo-romanelli/essentia/tree/music_extractor_nofail

To compile it, follow the instructions on the Essentia website (http://essentia.upf.edu/documentation/installing.html).
