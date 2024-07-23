#!/usr/bin/env python3

import pygame

# helper functions for a GUI


def add_border(base_image, border, border_image):
    xsize = base_image.get_width()
    ysize = base_image.get_height()
    # long routine
    added_border = border.border_size * 2
    xsize = max(border.dimensions.min_width, xsize + added_border)
    ysize = max(border.dimensions.min_height, ysize + added_border)
    # add the extra padding we need
    width = xsize + border.dimensions.extra_width
    height = ysize + border.dimensions.extra_height
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()

    # blit all the corners
    image.blit(border_image, (0, 0), pygame.Rect(border.rects.top_left))
    xpos = width - border.rects.top_right[2]
    image.blit(border_image, (xpos, 0), pygame.Rect(border.rects.top_right))
    ypos = height - border.rects.bottom_left[3]
    image.blit(border_image, (0, ypos), pygame.Rect(border.rects.bottom_left))
    xpos = width - border.rects.bottom_right[2]
    ypos = height - border.rects.bottom_right[3]
    image.blit(border_image, (xpos, ypos), pygame.Rect(border.rects.bottom_right))

    # iterate for top window
    border_width = width - (border.rects.top_left[2] + border.rects.top_right[2])
    top = pygame.Surface((border_width, border.rects.top_middle[3]))
    xpos = 0
    blit_rect = pygame.Rect(border.rects.top_middle)
    while xpos < top.get_width():
        top.blit(border_image, (xpos, 0), blit_rect)
        xpos += blit_rect.width
    image.blit(top, (border.rects.top_right[2], 0))

    # and then for the bottom
    border_width = width - (border.rects.bottom_left[2] + border.rects.bottom_right[2])
    bottom = pygame.Surface((border_width, border.rects.bottom_middle[3]))
    xpos = 0
    blit_rect = pygame.Rect(border.rects.bottom_middle)
    while xpos < bottom.get_width():
        bottom.blit(border_image, (xpos, 0), blit_rect)
        xpos += blit_rect.width
    xpos = border.rects.bottom_middle[0]
    ypos = image.get_height() - border.rects.bottom_middle[3]
    image.blit(bottom, (xpos, ypos))

    # and then the left
    border_height = height - (border.rects.top_left[3] + border.rects.bottom_left[3])
    left = pygame.Surface((border.rects.middle_left[2], border_height))
    ypos = 0
    blit_rect = pygame.Rect(border.rects.middle_left)
    while ypos < left.get_height():
        left.blit(border_image, (0, ypos), blit_rect)
        ypos += blit_rect.height
    ypos = border.rects.top_left[3]
    image.blit(left, (0, ypos))

    # and then the right
    border_height = height - (border.rects.top_right[3] + border.rects.bottom_right[3])
    right = pygame.Surface((border.rects.middle_right[2], border_height))
    ypos = 0
    blit_rect = pygame.Rect(border.rects.middle_right)
    while ypos < right.get_height():
        right.blit(border_image, (0, ypos), blit_rect)
        ypos += blit_rect.height
    xpos = image.get_width() - border.rects.middle_right[2]
    ypos = border.rects.top_right[3]
    image.blit(right, (xpos, ypos))

    # blit the background
    pos = pygame.Rect(border.rects.middle_right[2], border.rects.top_middle[3], xsize, ysize)
    pygame.draw.rect(image, border.background, pos)

    # now draw the contents
    pos = (pos.x + border.border_size, pos.y + border.border_size)
    image.blit(base_image, pos)
    return image
