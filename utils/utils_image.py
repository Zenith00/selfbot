from PIL import Image
import requests
from io import BytesIO
import struct
# import Image
import scipy
import scipy.misc
import scipy.cluster

def average_color_url(url):
    NUM_CLUSTERS = 5
    response = requests.get(url)
    im = Image.open(BytesIO(response.content))
    im = im.resize((150, 150))      # optional, to reduce time
    ar = scipy.misc.fromimage(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2])

    codes, dist = scipy.cluster.vq.kmeans(ar.astype(float), NUM_CLUSTERS)
    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

    index_max = scipy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    peak = peak.astype(int)
    colour = ''.join(format(c, '02x') for c in peak)
    return colour[0:6]

# average_color_url(" https://images.discordapp.net/avatars/129706966460137472/3db67b0f41b3b9de89469c63040fa918")


