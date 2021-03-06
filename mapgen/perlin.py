# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 22:13:56 2020

@author: Christian Konstantinov
"""
import numpy as np

def noise(n, fs, f0):
    "Generate Perlin Noise of length n with fundamental f0 sampled at fs Hz."
    noise = np.zeros((n,), np.float32)
    Td = n // f0 # bracket length in samples.
    # create random noise [-1, 1)
    g = np.random.uniform(low=0, high=1, size=n) * 2 - 1
    # create brackets
    bxi = np.array([x for x in np.arange(0, n, Td)])
    for i in np.arange(n):
        bx0 = bxi[i // Td] # left bracket bound
        bx1 = (bx0 + 1) % n # right bracket bound
        rx0 = (i % Td) / Td # distance from bx0 to i
        rx1 = rx0 - 1 # distance from bx1 to i
        u = rx0 * g[bx0]
        v = rx1 * g[bx1]
        sx = interpolate(0, 1, rx0, 'cubic')
        noise[i] = interpolate(u, v, sx, 'linear')
    return noise

def generate(n, fs, p, o, f0=1):
    """
    Generate Perlin Noise of length n, sample rate fs, fundamental frequency f0,
    persistence p, and o octaves.

    Parameters
    ----------
    n : int
        Noise length in samples.
    fs : int
        Sample rate in Hz.
    p : float
        Persistence.
        A coefficient between (0, 1] which determines amplitude at each octave.
    o : int
        Octaves.
        The number of harmonics added to the output noise sequence.
    f0 : int
        Fundamental Frequency.
        A coefficient for the frequency which determines bracket density.
        The default is 1.

    Returns
    -------
    perlin : numpy.ndarray
        The generated Perlin Noise Sequence.

    """
    freq = [2**i for i in range(o)]
    amp = np.array([p**i for i in range(o)])
    perlin = np.zeros((n, o), np.float32)
    for i in np.arange(o):
        perlin[:, i] = noise(n, fs, (f0*freq[i])%n)
    perlin = np.sum(np.multiply(perlin, amp.T), axis=1)
    return normalize(perlin)

def interpolate(p, q, s, method):
    """Interpolate between p and q at s using the selected method."""
    if method == 'linear':
        return p * (1 - s) + q * s
    elif method == 'cosine':
        ft = s * np.pi
        f = (1 - np.cos(ft)) * 0.5
        return p * (1 - f) + q * f
    elif method == 'cubic':
        f = 3 * s**2 - 2 * s**3
        return p * (1 - f) + q * f
    else:
        return 0

def normalize(input_sig):
    """Normalize to [-1, 1]"""
    return input_sig / np.max(np.abs(input_sig))

#%%

if __name__ == '__main__':
    import onset_detect as od
    import scipy.io.wavfile as wf
    import matplotlib.pyplot as plt

    fs, input_sig = wf.read('./mapgen/test/perlin.wav')
    if input_sig.ndim > 1:
        input_sig = input_sig[:, 0] + input_sig[:, 1]

    onsets = od.superflux(fs, input_sig)
    perlin_noise = generate(len(onsets), fs, 0.5, 6, f0=128)

    plt.figure()
    plt.vlines(onsets, 0, 1.0, color='black')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Onsets')

    plt.figure()
    plt.plot(perlin_noise)
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.title('Onset Generated Perlin Noise')