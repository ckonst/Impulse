# Impulse
Impulse is a rhythm game where the player must click on the circles that appear on the screen to the beat of the song. Players can play procedurally generated beatmaps using their own audio files.

The beatmaps are automatically generated using superflux onset detection, and Perlin Noise for x and y coordinates.

![mel spectrogram](https://raw.githubusercontent.com/ckonst/Impulse/master/Impulse/data/assets/img/log-mel-fs.png)

For onset detection, a log mel-spectrogram is taken from the user's selected audio file. A window length of 1024 samples with a stride of 441 samples is used at a sampling frequency of 44100 Hz.

![superflux onsets](https://raw.githubusercontent.com/ckonst/Impulse/master/Impulse/data/assets/img/superflux-onsets.png)

Next the superflux function is applied to generate peaks for the peak picking onset detection function.

Lastly, two Perlin Noise sequences are constructed for the x and y coordinates for each onset.

![perlin noise](https://raw.githubusercontent.com/ckonst/Impulse/master/Impulse/data/assets/img/perlin.png)

Each beatmap is stored in its own folder under `/Impulse/data/beatmaps/` using the name of the input file. A json file is created containing the name of the song, list of onsets and corresponding x and y locations.

![title screen](https://raw.githubusercontent.com/ckonst/Impulse/master/Impulse/data/assets/img/Impulse.png)


