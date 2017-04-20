filepath = None
fileExists = False
fileSize = 0

import sys


def formatName(name):
    return " ".join(name.split()[:3])


def getVid(url):
    from os import path
    from pytube import YouTube

    global filepath

    youtube = YouTube(url)
    video = youtube.filter('mp4')[0]
    filepath = "./%s.mp4" % formatName(video.filename)

    if path.exists(filepath):
        print("Video already exists.")
        global fileExists
        fileExists = True
        return
    else:
        print("Downloading video...")
        video.download(filepath)
        print("Download complete.")


def averages():
    import imageio
    import numpy as np
    reader = imageio.get_reader(filepath)
    yield len(reader)
    try:
        for frame in reader:
            yield (np.mean(frame, axis=(0, 1), dtype=np.float32))
    except:
        return


def show(limit=None, height=100):
    import matplotlib.pyplot as plt
    import numpy as np

    colors = averages()
    plt.xlim(xmax=next(colors))
    plt.ylim(ymax=height)

    for i, x in enumerate(colors):
        if limit:
            if i == limit:
                break
        r, g, b = x
        r = min(r, 255)
        g = min(g, 255)
        b = min(b, 255)
        plt.plot([i, i], [0, height], color=(r / 255, g / 255, b / 255, 1))
    plt.show()


if __name__ == "__main__":
    print("Getting video...")
    getVid(sys.argv[1])
    print("Calculating frame averages...")
    show(height=50)
    print("Done.")
