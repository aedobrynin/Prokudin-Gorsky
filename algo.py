import threading
import sys
import os
import skimage
import skimage.io
import skimage.color
import skimage.transform
import numpy
import warnings
from time import time


class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return


def get_the_best_shifts(channel_a, channel_b, row_shift_search_range,
                        col_shift_search_range):
    """The function brute forcing row and column shifts for channel_a and
    finding such a shift that gives the maximal correlation coefficient."""

    min_row_shift, max_row_shift = row_shift_search_range
    min_col_shift, max_col_shift = col_shift_search_range

    max_correlation = None
    the_best_row_shift = min_row_shift - 1
    the_best_col_shift = min_col_shift - 1

    channel_a_shifted = numpy.roll(
        channel_a, (min_row_shift - 1, min_col_shift - 1), axis=(0, 1))

    direction = -1

    """Brute force search to find the best shifts"""
    for row_shift in range(min_row_shift, max_row_shift + 1):
        channel_a_shifted = numpy.roll(channel_a_shifted, 1, axis=0)

        """Entering rolling direction helps to speed up algorithm.
           We making numpy roll only for one column every iteration
           instead rolling the whole channel on min_col_shift."""

        direction = -direction

        if direction == -1:
            min_col_shift, max_col_shift = max_col_shift, min_col_shift

        for col_shift in range(min_col_shift, max_col_shift + direction,
                               direction):
            channel_a_shifted = numpy.roll(
                channel_a_shifted, direction, axis=1)

            cur_correlation = (channel_a_shifted * channel_b).sum()

            if max_correlation is None or cur_correlation > max_correlation:
                max_correlation = cur_correlation

                the_best_row_shift = row_shift
                the_best_col_shift = col_shift

        if direction == -1:
            min_col_shift, max_col_shift = max_col_shift, min_col_shift

    return (the_best_row_shift, the_best_col_shift)


def pyramid_shifts_search(channel_a, channel_b):
    """Searching the best shift for channel_a to rich the maximal
    correlation coefficient with channel_b.
    The function uses image pyramid to solve the problem."""

    """Setting image pyramid's depth"""
    depth = 3
    if channel_a.shape[0] > 1000 and channel_a.shape[1] > 1000:
        depth = 5

    """Creating image pyramids"""
    channel_a_pyramid = tuple(skimage.transform.pyramid_gaussian(
        channel_a, max_layer=depth, downscale=2, multichannel=False))
    channel_b_pyramid = tuple(skimage.transform.pyramid_gaussian(
        channel_b, max_layer=depth, downscale=2, multichannel=False))

    row_shift_search_range = (-7, 7)
    col_shift_search_range = (-7, 7)

    """Calculating the best shifts from the smallest to the largest image"""
    for cur_a, cur_b in reversed(tuple(zip(channel_a_pyramid,
                                           channel_b_pyramid))):
        the_best_shifts = get_the_best_shifts(cur_a, cur_b,
                                              row_shift_search_range,
                                              col_shift_search_range)

        """Transition to larger image"""
        row_shift_search_range = (the_best_shifts[0] * 2 - 2,
                                  the_best_shifts[0] * 2 + 2)
        col_shift_search_range = (the_best_shifts[1] * 2 - 2,
                                  the_best_shifts[1] * 2 + 2)

    return the_best_shifts


def main(path):
    img = skimage.img_as_float(skimage.io.imread(path))

    img_r, img_c = img.shape[:2]
    img_r -= img_r % 3

    cut = 0.1
    channel_row_cut = int(img_r // 3 * cut)
    channel_col_cut = int(img_c * cut)
    channel_size = img_r // 3

    """Splitting image into 3 channels (Blue, Green, Red) and getting rid
    of borders."""
    b = img[channel_row_cut: channel_size - channel_row_cut,
            channel_col_cut: -channel_col_cut]

    g = img[channel_size + channel_row_cut: 2 * channel_size - channel_row_cut,
            channel_col_cut: -channel_col_cut]

    r = img[2 * channel_size + channel_row_cut: img_r - channel_row_cut,
            channel_col_cut: -channel_col_cut]

    """Setting up two threads to calculate the best shifts using image
    pyramid"""
    find_the_best_b_shifts_thread = ThreadWithReturnValue(
        target=pyramid_shifts_search, args=(b, g))

    find_the_best_r_shifts_thread = ThreadWithReturnValue(
        target=pyramid_shifts_search, args=(r, g))

    find_the_best_b_shifts_thread.start()
    find_the_best_r_shifts_thread.start()

    b_shifts = find_the_best_b_shifts_thread.join()
    r_shifts = find_the_best_r_shifts_thread.join()

    b = numpy.roll(b, b_shifts, axis=(0, 1))
    r = numpy.roll(r, r_shifts, axis=(0, 1))

    """Calculating final image size"""
    total_cut = (max(abs(b_shifts[0]), abs(r_shifts[0])), max(
        abs(b_shifts[1]), abs(r_shifts[1])))

    """Substraction in slices needs for cases
    when total_cut[0] or total_cut[1] == 0"""
    b = b[total_cut[0]: b.shape[0] - total_cut[0],
          total_cut[1]: b.shape[1] - total_cut[1]]
    g = g[total_cut[0]: g.shape[0] - total_cut[0],
          total_cut[1]: g.shape[1] - total_cut[1]]
    r = r[total_cut[0]: r.shape[0] - total_cut[0],
          total_cut[1]: r.shape[1] - total_cut[1]]

    """Saving final image"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        skimage.io.imsave(
            "result/" + path[path.rfind('/') + 1:],
            skimage.img_as_uint(numpy.dstack((r, g, b))))


if __name__ == "__main__":
    if "result" in os.listdir("./"):
        already_colored = os.listdir("./result")
    else:
        os.mkdir("./result")
        already_colored = []

    for path in sys.argv[1:]:
        try:
            print(f"Started to work with {path}!", end=' ', flush=True)

            if path[path.rfind('/') + 1:] in already_colored:
                print(f"Skipping {path}, because already colored")
                continue

            start_time = time()
            main(path)
            print(f"Time spent: {round(time() - start_time, 3)} sec.",
                  flush=True)
        except FileNotFoundError:
            print(f'File with path "{path}" not found!')
