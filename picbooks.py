#!/usr/bin/python3

import json
import math
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1024, 735))
#screen = pygame.display.set_mode((2048, 1470))
running = True

background = pygame.image.load("old-book-open.jpg")
right_arrow = pygame.image.load("right-arrow.png")

legend = pygame.font.Font("Rockybilly.ttf", 24)

scale_by = min(screen.get_width()/background.get_width(), screen.get_height()/background.get_height())

background = pygame.transform.scale_by(background, scale_by)
right_arrow = pygame.transform.scale_by(right_arrow, scale_by)
left_arrow = pygame.transform.flip(right_arrow, flip_x=True, flip_y=False)

total_images = 351
images_per_page = 12
page = 0
last_page = math.ceil(total_images / images_per_page) - 1
image_width = 0.15
image_height = 0.15

page_num1_pos = (0.1, 0.9)
page_num2_pos = (0.9, 0.9)

left_arrow_x = 0.25
right_arrow_x = 0.7
arrows_y = 0.9

frame_offsets_px = [
    (102, 72), #(144, 139),
    (75, 55), #(110, 107),
    (43, 42), #( 62,  78),
    (75, 55), #(114, 111),
    (75, 55), #(110, 107),
]

frame_offsets = [(fo[0]/2650, fo[1]/1900) for fo in frame_offsets_px]


def scale_pos(pos):
    return (int(background.get_width()*pos[0]), int(background.get_height()*pos[1]))


def shift_pos(pos, shift):
    return (pos[0]-shift[0], pos[1]-shift[1])

def load_frame(num):
    frame = pygame.image.load("frame%d.png" % num)
    # The frames have an inner size of ~600x600
    # We want the frame to be scaled so that this inner size fits an image.
    ratio = (frame.get_width()/600, frame.get_height()/600)
    to_size_inner = scale_pos((image_width, image_height))
    to_size_outer = (ratio[0]*to_size_inner[0], ratio[1]*to_size_inner[1])

    return pygame.transform.scale(frame, to_size_outer)


frames = [
    load_frame(1),
    load_frame(2),
    load_frame(3),
    load_frame(4),
    # TODO: Find a 5th frame rather than reusing the same twice.
    # Having 3 or 4 frames means that the layout doesn't change when we change
    # page (as there are 12 pictures per page)
    load_frame(2),
]

pos_images = [
    (0.11, 0.1),
    (0.31, 0.1),
    (0.11, 0.38),
    (0.31, 0.38),
    (0.11, 0.66),
    (0.31, 0.66),
    (0.53, 0.1),
    (0.73, 0.1),
    (0.53, 0.38),
    (0.73, 0.38),
    (0.53, 0.66),
    (0.73, 0.66),
]

progress = {
    "images": {},
    "total_words": 0,
}
if os.path.isfile("images/progress.json"):
    progress = json.load(open("images/progress.json"))

show_picture = None

while running:
    left_arrow_pos = scale_pos((left_arrow_x, arrows_y))
    right_arrow_pos = scale_pos((right_arrow_x, arrows_y))
    left_arrow_rect = pygame.Rect(left_arrow_pos, left_arrow.get_size())
    right_arrow_rect = pygame.Rect(right_arrow_pos, right_arrow.get_size())

    clicked = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if show_picture:
                    show_picture = None
                else:
                    x, y = event.pos
                    if left_arrow_rect.collidepoint((x, y)) and page > 0:
                        page -= 1
                    elif right_arrow_rect.collidepoint((x, y)) and page < last_page:
                        page += 1
                    else:
                        clicked = (x, y)

    screen.fill("black")

    screen.blit(background, (0, 0))

    screen.blit(left_arrow, left_arrow_pos)
    screen.blit(right_arrow, right_arrow_pos)

    for i in range(images_per_page):
        img = i + page*images_per_page + 1
        if img > total_images:
            break
        image_file = None
        if str(img) in progress["images"]:
            image_file = "images/%s" % progress["images"][str(img)]["path"]
            image = pygame.image.load(image_file)
            image = pygame.transform.scale(image, scale_pos((image_width, image_height)))
            image_pos = scale_pos(pos_images[i])
            screen.blit(image, image_pos)
            image_rect = pygame.Rect(image_pos, image.get_size())

            if clicked and image_rect.collidepoint(clicked):
                show_picture = image_file
                clicked = None

        frame_idx = img%len(frames)
        screen.blit(frames[frame_idx], scale_pos(shift_pos(pos_images[i], frame_offsets[frame_idx])))

    page_num1 = pygame.transform.scale_by(legend.render("%d" % (2*page+1), True, "black"), scale_by)
    page_num2 = pygame.transform.scale_by(legend.render("%d" % (2*page+2), True, "black"), scale_by)

    screen.blit(page_num1, scale_pos(page_num1_pos))
    screen.blit(page_num2, scale_pos(page_num2_pos))

    if show_picture:
        image = pygame.image.load(show_picture)
        screen.blit(image, ((screen.get_width() - image.get_width()) / 2, (screen.get_height() - image.get_height()) / 2))

    pygame.display.flip()

pygame.quit()
