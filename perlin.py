from colorsys import hsv_to_rgb
import tkinter
import noise

dimensions = [400, 300]
pixel_scale = 10
perlin_scale = 4

off = [0, 0, 0]

root = tkinter.Tk()
root.title("Perlin noise")
display = tkinter.Canvas(root, width=dimensions[0], height=dimensions[1], highlightthickness=0)
display.pack()

def rgb_to_hex(r, g, b):
    return "#" + hex(int(r))[2:].zfill(2) + hex(int(g))[2:].zfill(2) + hex(int(b))[2:].zfill(2)


def update():
    display.delete("all")
    for x in range(dimensions[0]//pixel_scale):
        for y in range(dimensions[1]//pixel_scale):
            ix = x / dimensions[0] * pixel_scale * perlin_scale
            iy = y / dimensions[1] * pixel_scale * perlin_scale

            col = rgb_to_hex(*hsv_to_rgb(0, 0, 50*(1+noise.pnoise3(ix + off[0], iy + off[1], off[2]))))
            display.create_rectangle(x * pixel_scale, y * pixel_scale, (x + 1) * pixel_scale, (y + 1) * pixel_scale, fill=col, outline="")

    off[0] += 0.02
    off[1] += 0.02
    off[2] += 0.02

    root.after(100, update)

root.after_idle(update)
root.mainloop()
