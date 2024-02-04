from functools import wraps
import timeit
import Impulse.mapgen.onset_detect as od
from Impulse.mapgen import perlin
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt


def timed(f):
    """Measure the time it takes for f to execute."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        result = f(*args, **kwargs)
        end = timeit.default_timer()
        elapsed = (end - start) * 1_000_000
        print('Elapsed time: {} microsecs'.format(elapsed))
        return elapsed, result

    return wrapper


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


def test_noise_performance():
    fs, input_sig = wf.read('./tests/data/audio/large/5. ambedo 2MASTER.wav')
    if input_sig.ndim > 1:
        input_sig = input_sig[:, 0] + input_sig[:, 1]

    onsets = od.superflux(fs, input_sig)

    _sum = 0
    runs = 10
    for i in range(runs):
        time, _ = get_noise(onsets, fs)
        _sum += time

    print(_sum / runs)


@timed
def get_noise(onsets, fs):
    return perlin.generate(len(onsets), fs, 0.5, 6, f0=128)
