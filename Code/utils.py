import glob
import importlib
from pathlib import Path

from telethon import events

from Code import bot


def Mbot(**args):
    pattern = args.get("pattern", None)
    r_pattern = r"^[/?!.]"
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern
    args["pattern"] = pattern.replace("^/", r_pattern, 1)

    def decorator(func):
        bot.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator


def Cbq(**args):
    def decorator(func):
        bot.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator


def load_module(name):
    import Code.utils  # pylint:disable=E0602

    path = Path(f"Code/modules/{name}.py")
    nname = "Code.modules.{}".format(name)
    spec = importlib.util.spec_from_file_location(nname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    print("imported " + name)


for name in glob.glob("modules/modules/*.py"):
    with open(name) as f:
        load_module((Path(f.name)).stem.replace(".py", ""))
