
from libs.API import API

api = API()

def reset_if_not_on_cooldown(ctx):
    """ Only reset the cooldown if we were not on cooldown before. """
    if not ctx.command.is_on_cooldown(ctx):
        ctx.command.reset_cooldown(ctx)
