import os
import math

import matplotlib.image as mpimg
import numpy


def pos_map(pos):
    return pos if pos < 2 else pos + 1


def stitch(dir, x_interval, y_interval, backend = ".png", num_x = None,
           files = None):
    filenames_ = os.listdir(dir) if files is None else files
    filenames = [os.path.join(dir, x) for x in filenames_]
    filenames = list(filter(lambda x: x.endswith(backend), filenames))
    res: numpy.ndarray
    res = None
    if num_x is None:
        num_x = math.ceil(math.sqrt(len(filenames)))
    num_y = math.ceil(len(filenames) / num_x)

    for idx, file in enumerate(filenames):
        if "HGG" in dir:
            idx = pos_map(idx)

        cdata = mpimg.imread(file)
        shape = cdata.shape
        y, x, c = shape

        if res is None:
            res = numpy.ones(((y_interval + y) * num_y, (x + x_interval) * num_x, c))
        x_pos_int, y_pos_int = idx % num_x, idx // num_x

        x_pos = x_pos_int * (x + x_interval)
        if "HGG" in dir and y_pos_int != 1:
            x_pos += (x + x_interval) // 2
        y_pos = y_pos_int * (y + y_interval)
        res[y_pos:y_pos + y, x_pos:x_pos + x, :] = cdata
        # res[y_pos:y_pos + y, x_pos:x_pos + x, :] = cdata
    mpimg.imsave(dir + ".png", res)
    return res


if __name__ == '__main__':
    for dir_ in os.listdir("剪裁"):
        dir = os.path.join("剪裁", dir_)
        if os.path.isfile(dir):
            continue
        if dir_ == "DL GBM":
            stitch(dir, 10, 100, num_x = 2)
            continue
        stitch(dir, 10, 100)
