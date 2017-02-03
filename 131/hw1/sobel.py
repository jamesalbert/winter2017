from PIL import Image
import itertools


img = Image.open('space.jpg')
img.convert('P')
pixels = img.load()
width, height = img.size


gradient = ((-1, -2, -1),
            (0, 0, 0),
            (1, 2, 1))


def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def sobel(w, h):
    g = dict()
    for i in range(3):
        g[f"p{i + 1}"] = pixels[w + i, h][0]
        g[f"p{i + 4}"] = pixels[w + i, h + 1][0]
        g[f"p{i + 7}"] = pixels[w + i, h + 2][0]
    G = abs((g['p1'] + 2 * g['p2'] + g['p3']) -
            (g['p7'] + 2 * g['p8'] + g['p9'])) + \
        abs((g['p3'] + 2 * g['p6'] + g['p9']) -
            (g['p1'] + 2 * g['p4'] + g['p7']))
    return (G, G, G)


if __name__ == '__main__':
    for w in range(0, width, 3):
        for h in range(0, height, 3):
            print(1)
            if w + 3 > width and h + 2 > h:
                print(0)
                break
            pixel = sobel(w, h)
            for i in range(3):
                pixels[w + i, h] = pixel
                pixels[w + i, h + 1] = pixel
                pixels[w + i, h + 2] = pixel

    img.save('sobel_space.jpg')
