import os
import time
import eyed3

start = time.time()
print(
    "This program changes the ID3 tags of all .mp3 files "
    "in this directory.\n"
    + 'The files have to have the format "<song name> - <song artist>.mp3"'
)
mp3files = [f for f in os.listdir() if f[-4:] == ".mp3"]
# files have any of those featuring tags to indicate that the next name is
# a featuring author
features = [
    "featuring",
    "feat.",
    "ft.",
    "FT.",
    "FEAT.",
    "feat",
    "ft",
    "FT",
    "FEAT",
    "Feat.",
    "Feat",
]

# a list that keeps track of all of the files that were incorrectly named.
# this is useful to keep track of, since those files can be changed manually.
incorrect_files = list()
for f in mp3files:
    # format of filename: <song_name> - <song_artist>.mp3 (including space)
    text = f.split(" - ")
    if not len(text) == 2:
        # incorrect format, skip this file
        print(f"Tag of file '{f}' won't be changed, the format is incorrect")
        incorrect_files.append(f)
        continue

    artist = text[0]  # <song_name>
    rest = text[1][:-4]  # <song_artist>, without .mp3
    title = None
    # determine if one of the feature texts is in the song artist part
    has_feature = any([feature in rest for feature in features])
    if has_feature:
        feature_text = [x for x in features if x in rest][0]  # get feat. text
        splitted = rest.split(feature_text)
        title = splitted[0]
        featured_artist = splitted[1]
        artist += " ft." + featured_artist

    if not title:
        title = rest

    audiofile = eyed3.load(f)
    try:
        audiofile.tag.artist, audiofile.tag.title = artist, title
        audiofile.tag.save()
        os.rename(f, title + ".mp3")
    except eyed3.Error:
        # unknown why, this happens when eye3d throws an error (audiofile.tag
        # is None, not sure what makes this happen)
        print(f"Error in file {f}")
        incorrect_files.append(f)

if incorrect_files:
    print(
        f"There were {len(incorrect_files)} incorrectly named files:\n"
        f"{incorrect_files}"
    )

print(
    f"Changed tags of {len(mp3files) - len(incorrect_files)} files. "
    f"It took {time.time() - start:.3} seconds."
)
