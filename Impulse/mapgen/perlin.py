import numpy as np
from numba import njit


@njit
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
    for i in range(o):
        perlin[:, i] = noise(n, fs, (f0 * freq[i]) % n)
    perlin = np.sum(np.multiply(perlin, amp.T), axis=1)
    return peak_normalize(perlin)


@njit
def noise(n, fs, f0):
    "Generate Perlin Noise of length n with fundamental f0 sampled at fs Hz."
    noise = np.zeros((n, ), np.float32)
    Td = n // f0  # bracket length in samples.
    # create random noise [-1, 1)
    g = np.random.uniform(low=0, high=1, size=n) * 2 - 1
    # create brackets
    bxi = np.array([x for x in np.arange(0, n, Td)])
    for i in range(n):
        bx0 = bxi[i // Td]  # left bracket bound
        bx1 = (bx0 + 1) % n  # right bracket bound
        rx0 = (i % Td) / Td  # distance from bx0 to i
        rx1 = rx0 - 1  # distance from bx1 to i
        u = rx0 * g[bx0]
        v = rx1 * g[bx1]
        sx = interpolate_cubic(0, 1, rx0)
        noise[i] = interpolate_linear(u, v, sx)
    return noise


@njit
def interpolate_linear(p, q, s):
    """Interpolate between p and q at s using a linear model."""
    return p * (1 - s) + q * s


@njit
def interpolate_cosine(p, q, s):
    """Interpolate between p and q at s using a cosine model."""
    ft = s * np.pi
    f = (1 - np.cos(ft)) * 0.5
    return p * (1 - f) + q * f


@njit
def interpolate_cubic(p, q, s):
    """Interpolate between p and q at s using a cubic model."""
    f = 3 * s**2 - 2 * s**3
    return p * (1 - f) + q * f


@njit
def peak_normalize(input_sig):
    """Peak Normalize to [-1, 1]"""
    return input_sig / np.max(np.abs(input_sig))
