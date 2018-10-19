pyrat - Raw Audio Tools v0.1
===================================

Raw tools for raw audio.

The tools are intended to be fast, simple and entirely non-interactive.  To
avoid doing what other applications are much better at (e.g. sox), the input
and output data is always assumed to be a 1-channel (mono) stream of 32-bit
float samples.  If you have a FLAC stereo file, for example, and you want to
convert it to the raw format, use sox:

> sox -t flac -c 2 INFILE -t f32 -c 1 OUTFILE_ch1.raw remix 1
> sox -t flac -c 2 INFILE -t f32 -c 1 OUTFILE_ch2.raw remix 2

Then process the two raw files concurrently.


Dependencies
------------

- Python3
- NumPy and SciPy libraries


Tools
-----

- conv    -- convolve two signals
- randph  -- randomize phases of FFT coefficients.


License
-------

MIT, of course. See LICENSE file.