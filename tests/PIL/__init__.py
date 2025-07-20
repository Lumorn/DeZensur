from types import SimpleNamespace


class Image(SimpleNamespace):
    def __init__(self, size=(10, 10)):
        super().__init__(size=size)

    @staticmethod
    def open(path):
        return Image()

    def convert(self, mode):
        return self

    def resize(self, size):
        self.size = size
        return self

    def copy(self):
        return Image(self.size)

    def crop(self, box):
        return Image((box[2] - box[0], box[3] - box[1]))

    def paste(self, img, pos):
        pass

    def thumbnail(self, size):
        pass

    def save(self, fp, format=None):
        with open(fp, "wb") as f:
            f.write(b"0")

    @staticmethod
    def new(mode, size, color=None):
        return Image(size)

    def filter(self, *args, **kwargs):
        return self

    @staticmethod
    def composite(im1, im2, mask):
        return im1

    @staticmethod
    def blend(im1, im2, alpha):
        return im1


class ImageFilter:
    class GaussianBlur:
        def __init__(self, radius):
            self.radius = radius

    @staticmethod
    def new(mode, size, color=None):
        return Image(size)


def new(mode, size, color=None):
    return Image.new(mode, size, color)
