from PIL import Image
from math import cos, sin, pi
from tqdm import tqdm

colorA = "#32cd32"  # first color
colorB = "#ff32cd"  # second color
angle = 45  # angle of the gradient in degrees
width = 1920  # width of gradient
height = 1080  # height of gradient

width = int(width/2)
height = int(height/2)

list_imgs = []

save_gif = 0


def rgb2cmyk(color: list):
    r = color[0]
    g = color[1]
    b = color[2]
    _R = r / 255
    _G = g / 255
    _B = b / 55
    K = 1 - max(_R, _G, _B)
    C = (1 - _R - K) / (1 - K)
    M = (1 - _G - K) / (1 - K)
    Y = (1 - _B - K) / (1 - K)
    return [int(C * 100), int(M * 100), int(Y * 100), int(K * 100)]


def cmyk2rgb(color: list):
    _C = color[0]
    _M = color[1]
    _Y = color[2]
    _K = color[3]
    R = 255 * (1 - _C) * (1 - _K)
    G = 255 * (1 - _M) * (1 - _K)
    B = 255 * (1 - _Y) * (1 - _K)
    return [R, G, B]


def hex2rgb(color: str):
    if color.startswith('#'):
        color = color.split("#")[1]
    if len(color) == 8:
        return hex2rgba(color)
    else:
        __red = int(color[:2], 16)
        __green = int(color[2:4], 16)
        __blue = int(color[4:6], 16)
    return [__red, __green, __blue]


def hex2rgba(color: str):
    if color.startswith('#'):
        color = color.split("#")[1]
    if len(color) == 6:
        return hex2rgb(color)
    else:
        __alpha = int(color[:2], 16)
        __red = int(color[2:4], 16)
        __green = int(color[4:6], 16)
        __blue = int(color[6:8], 16)
    return [__red, __green, __blue, __alpha]


def mix2colors_rgb(colorA: list, colorB: list, amount: float):
    return [int((colorA[0] * (1 - amount) + colorB[0] * amount) + 0.5),
            int((colorA[1] * (1 - amount) + colorB[1] * amount) + 0.5),
            int((colorA[2] * (1 - amount) + colorB[2] * amount) + 0.5)]


def mix2colors_cmyk(colorA: list, colorB: list, amount: float):
    return [int((colorA[0] * (1 - amount) + colorB[0] * amount) + 0.5),
            int((colorA[1] * (1 - amount) + colorB[1] * amount) + 0.5),
            int((colorA[2] * (1 - amount) + colorB[2] * amount) + 0.5),
            int((colorA[3] * (1 - amount) + colorB[3] * amount) + 0.5)]


def calculateAngleData(angle):
    angle %= 360
    _a = sin(pi * angle / 180)
    _b = sin(pi * (angle / 180 + 0.5))
    _c = 1 / max(abs(cos(pi * angle / 180)), abs(sin(pi * angle / 180)))
    return [_a, _b, _c]


def calculateAmount(a, b, c, x, y):
    return (((x / width) - 0.5) * a + ((y / height) + 0.5) * b) / c


if __name__ == "__main__":
    colorA = hex2rgb(colorA)
    colorB = hex2rgb(colorB)
    for i in tqdm(range(0, 360, 45)):
        a, b, c = calculateAngleData(i)

        g_img = Image.new(mode="RGBA", size=(width, height))

        for x in range(width):
            for y in range(height):
                g_img.putpixel((x, y), tuple(mix2colors_rgb(colorA, colorB, calculateAmount(a, b, c, x, y))))

        # g_img.show()
        list_imgs.append(g_img)

        del g_img

    if save_gif:
        list_imgs.pop(0).save("./images/img.gif", format="GIF", append_images=list_imgs, save_all=True, duration=40,
                              loop=0)
    else:
        for img in range(len(list_imgs)):
            number = '{:>03}'.format(img)
            list_imgs[img].save(f'./images/{number}.png')

    from sys import exit as baum;baum()

# top2botton            |   0,    0,    1 | x, sin(angle), cos(angle)
# lefttop2rightbotton   |   0,  0.5,  0.5 |
# left2right            |   0,    1,    0 |
# leftbottom2righttop   | 0.5,  0.5, -0.5 |
# bottom2top            |   1,    0,   -1 |
# rightbottom2lefttop   |   1, -0.5, -0.5 |
# right2left            |   1,   -1,    0 |
# righttop2leftbottom   | 0.5, -0.5,  0.5 |
