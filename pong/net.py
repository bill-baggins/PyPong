import pygame
from .options import OPTION


def create_net_texture(net_width: int, net_height: int):
    net = pygame.Surface([net_width, net_height])

    m_net_height = net_height // 10
    for y in range(m_net_height):
        if y % 2 == 0:
            net_rect = pygame.Rect(0, y * 10, net_width, 20)
            pygame.draw.rect(net,
                             OPTION["NET_COLOR"],
                             net_rect)
        else:
            pygame.draw.rect(net,
                             OPTION["BACKGROUND_COLOR"],
                             pygame.Rect(0, y * 10, 5, 20))

    return net


def draw_net(screen: pygame.Surface,
             net_texture: pygame.Surface,
             net_x: int,
             net_y: int):
    screen.blit(net_texture, [net_x, net_y])
