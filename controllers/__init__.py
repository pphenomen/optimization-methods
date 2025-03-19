from .lr1_controller import register_lr1_callbacks
from .lr2_controller import register_lr2_callbacks
from .lr3_controller import register_lr3_callbacks

def register_all_callbacks(app):
    register_lr1_callbacks(app)
    register_lr2_callbacks(app)
    register_lr3_callbacks(app)
