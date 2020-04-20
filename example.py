#!/usr/bin/env python

import tkinter as tk
import time

SCREEN_WIDTH  = 640
SCREEN_HEIGHT = 480

TITLE_Y = 20

FIELD_PADDING = 30
BORDER_WIDTH = 10
POINT_RADIUS = 20

FIELD_X = FIELD_PADDING
FIELD_Y = FIELD_PADDING + TITLE_Y
FIELD_WIDTH = SCREEN_WIDTH - FIELD_X - FIELD_PADDING
FIELD_HEIGHT = SCREEN_HEIGHT - FIELD_Y - FIELD_PADDING

POINT_ACCELERATION = 5

COLOR_BORDER = "#0000FF"
COLOR_FIELD  = "#00FF00"
COLOR_POINT  = "#FF0000"

root = tk.Tk()
root.title("tkinter demo")

canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

text = canvas.create_text(SCREEN_WIDTH/2, TITLE_Y,
                          text="Use arrows or WASD to accelerate the point, use mouse to move the point, use Esc to exit.")

border = canvas.create_rectangle(FIELD_X, FIELD_Y,
                                 FIELD_X + FIELD_WIDTH, FIELD_Y + FIELD_HEIGHT,
                                 fill=COLOR_BORDER, outline="")

field = canvas.create_rectangle(FIELD_X + BORDER_WIDTH, FIELD_Y + BORDER_WIDTH,
                                FIELD_X + FIELD_WIDTH - BORDER_WIDTH, FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH,
                                fill=COLOR_FIELD, outline="")


point_max_x = FIELD_X + FIELD_WIDTH - BORDER_WIDTH - POINT_RADIUS
point_max_y = FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH - POINT_RADIUS
point_min_x = FIELD_X + BORDER_WIDTH + POINT_RADIUS
point_min_y = FIELD_Y + BORDER_WIDTH + POINT_RADIUS


point_x = FIELD_X + FIELD_WIDTH/2
point_y = FIELD_Y + FIELD_HEIGHT/2
point = canvas.create_oval(point_x - POINT_RADIUS, point_y - POINT_RADIUS,
                           point_x + POINT_RADIUS, point_y + POINT_RADIUS,
                           fill=COLOR_POINT, outline="")

# Some speed for more dynamic demo.
speed_x = -2 * POINT_ACCELERATION
speed_y = -2 * POINT_ACCELERATION
last_time = None


def process_key(event):
    dsx, dsy = 0, 0

    # event.char - regular symbols
    # event.keysym - special keys
    if event.keysym == "Up" or event.char == "w":
        dsy = -1
    elif event.keysym == "Down" or event.char == "s":
        dsy = 1
    elif event.keysym == "Left" or event.char == "a":
        dsx = -1
    elif event.keysym == "Right" or event.char == "d":
        dsx = 1
    elif event.keysym == "Escape":
        root.quit()
        return

    global speed_x, speed_y
    speed_x += POINT_ACCELERATION * dsx
    speed_y += POINT_ACCELERATION * dsy


def process_mouse(event):
    global point_x, point_y
    if 0 <= event.x < SCREEN_WIDTH and 0 <= event.y < SCREEN_HEIGHT:
        # Filter out non-canvas clicks.
        point_x = event.x
        point_y = event.y

def update_physics():
    global last_time, point_x, point_y, speed_x, speed_y
    cur_time = time.time()
    if last_time:
        dt = cur_time - last_time
        dx = speed_x * dt
        dy = speed_y * dt
        point_x += dx
        point_y += dy

        if not (point_min_x <= point_x <= point_max_x):
            point_x = max(point_min_x, min(point_x, point_max_x))
            speed_x = -speed_x
        if not (point_min_y <= point_y <= point_max_y):
            point_y = max(point_min_y, min(point_y, point_max_y))
            speed_y = -speed_y

        canvas.coords(point, point_x - POINT_RADIUS, point_y - POINT_RADIUS,
                             point_x + POINT_RADIUS, point_y + POINT_RADIUS)

    last_time = cur_time

    # update physics as frequent as possible
    root.after(1, update_physics)


root.bind("<Key>", process_key)
root.bind("<Button-1>", process_mouse)

update_physics()
root.mainloop()

