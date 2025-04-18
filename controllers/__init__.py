from .lr1_controller import register_lr1_callbacks
from .lr2_controller import register_lr2_callbacks
from .lr3_controller import register_lr3_callbacks
from .lr4_controller import register_lr4_callbacks
from .lr5_controller import register_lr5_callbacks
from .lr6_controller import register_lr6_callbacks

def register_all_callbacks(app):
    register_lr1_callbacks(app)
    register_lr2_callbacks(app)
    register_lr3_callbacks(app)
    register_lr4_callbacks(app)
    register_lr5_callbacks(app)
    register_lr6_callbacks(app)
