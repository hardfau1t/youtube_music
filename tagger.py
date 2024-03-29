import eyed3
import os
import logging


def Tag(filename):
    # This function changes songs title so it is better to use this at the end
    special_chars = ["(", "["]  # Used to strip unnecessory song info in the filename.
    song_tag = eyed3.load(filename)
    tag = filename[:filename.rfind(".")]
    logging.debug(f"tag is : {tag}")
    try:
        artist, title = tag.split("-", maxsplit=1)
    except ValueError:
        try:
            artist, title = tag.split("\u2012", maxsplit=1)
        except ValueError:
            try:
                artist, title = tag.split("_", maxsplit=1)
            except ValueError:
                print("Couldn't get the artist name!!!")
                title = tag
                artist = ""

    logging.debug(f"artist: {artist}, title: {title}")
    for char in special_chars:
        if char in title:
            title = title[:title.index(char)]
    title = title.strip()
    artist = artist.strip()
    song_tag.tag.title = title
    song_tag.tag.artist = artist
    song_tag.tag.save()
    try:
        # if song name isn't changed os error will occur
        song_tag.rename(title)
    except OSError:
        os.replace(song_tag.path, f"/drives/storage/music/dup/{os.path.basename(song_tag.path)}")
        logging.warning(f"failed to write title, possible duplicate {title}")
        pass
    return title
