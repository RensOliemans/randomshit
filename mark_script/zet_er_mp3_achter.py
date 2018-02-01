import os

# zet er mp3 achter als het geen extensie heeft
for f in os.listdir():
    if '.' not in f:
        os.rename(f, f + '.mp3')
# haal de spatie weg als die voor de '.mp3' zit
for f in os.listdir():
    if f[-5:] == ' .mp3':
        os.remane(f, f[:-5] + f[-4:])
