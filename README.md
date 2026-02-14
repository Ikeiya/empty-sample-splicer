# empty-sample-splicer

When obtaining Hi-res FLAC files from Amazon Music in certain sources, the md5 of the obtained file is not identical with Hi-res FLAC files from other sources. This is a result of empty samples in the audio sample of the file, which must be removed for the file to be "bit-perfect".

This script is inspired by: https://nptr.cc/posts/2024-05/amazon-music-postprocess/

However, there are a few quality of life issues with nptr's powershell script.
1. Windows only, no linux support
2. No logging file to verify samples are actually skipped

To resolve these issues, I wrote empty-sample-splicer which addresses these issues:
1. Windows only -> Rewritten in python and compilable with any operating system
2. Logging file with file name, sample rate, samples skipped and comparison of md5 before and after splicing

Prerequisite:
FLAC and METAFLAC is required for the functioning of the script
