from enum import Enum


class Workers(Enum):
    camera_worker = 'camera_worker',
    frames_move_worker = 'frames_move_worker',
    timer_worker = 'timer_worker',
    compare_colors_worker = 'compare_colors_worker'
