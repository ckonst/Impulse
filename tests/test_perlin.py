import Impulse.mapgen.onset_detect as od
from Impulse.mapgen import perlin
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt


def test_perlin_noise():
    fs, input_sig = wf.read('./tests/data/audio/perlin.wav')
    if input_sig.ndim > 1:
        input_sig = input_sig[:, 0] + input_sig[:, 1]

    onsets = od.superflux(fs, input_sig)
    perlin_noise = perlin.generate(len(onsets), fs, 0.5, 6, f0=128)

    plt.figure()
    plt.vlines(onsets, 0, 1.0, color='black')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Onsets')

    plt.savefig('./tests/data/img/onsets.png')

    plt.figure()
    plt.plot(perlin_noise)
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.title('Onset Generated Perlin Noise')

    plt.savefig('./tests/data/img/perlin_noise.png')
