#!/usr/bin/env python
import traceback
import shutil
from sys import platform, stdout, stderr, exc_info

VERSION = "0.5.2"

XDEBUG = 0
DEBUG = 10
INFO = 20
WARNING = 30
WARN = WARNING
ERROR = 40
CRITICAL = 50
_level_names = {'XDEBUG': XDEBUG, 'DEBUG': DEBUG, 'INFO': INFO,
                'WARNING': WARNING, 'WARN': WARN, 'ERROR': ERROR, 'CRITICAL': CRITICAL}

GLOBAL_SCOPE = None  # The actual value

_thresholds = {None: XDEBUG}


def set_threshold(scope, level):
    if level in _level_names:
        level = _level_names[level]
    _thresholds[scope] = level


def _threshold(scope):
    if scope in _thresholds:
        return _thresholds[scope]
    else:
        return _thresholds[None]


def _should_print(scope, level):
    return level >= _threshold(scope)


class Signale:

    def __init__(self, opts={"scope": None, "underlined": False, "ansi": None}):

        self.options = opts

        if "custom" in opts:
            self.custom_loggers_conf = opts["custom"]
            for conf in self.custom_loggers_conf:
                func = lambda text="", prefix="", suffix="", level=conf["level"]: self.log(
                    text, prefix, suffix, conf, level)
                setattr(self, conf["name"], func)

        try:
            self.underlined = opts["underlined"]
        except KeyError:
            self.underlined = False

        try:
            scope = opts["scope"]
            if scope != None:
                self.scope = scope if scope != "" else "global"
            else:
                self.scope = None
        except KeyError:
            self.scope = None

        if platform == "win32":
            self.figures = {
                "pause": "||",
                "tick": '√',
                "cross": '×',
                "star": '*',
                "squareSmallFilled": '[█]',
                "play": '►',
                "bullet": '*',
                "ellipsis": '...',
                "pointerSmall": '»',
                "info": 'i',
                "warning": '‼',
                "heart": '♥',
                "radioOn": '(*)',
                "radioOff": '( )',
                "eyes": 'OO',
            }
        else:
            self.figures = {
                "pause": "||",
                "tick": '✔ ',
                "cross": '✖ ',
                "star": '★ ',
                "squareSmallFilled": '◼ ',
                "play": '▶ ',
                "bullet": '● ',
                "ellipsis": '… ',
                "pointerSmall": '›',
                "info": 'ℹ ',
                "warning": '⚠ ',
                "heart": '♥ ',
                "radioOn": '◉ ',
                "radioOff": '◯ ',
                "eyes": '👀',
            }

        self.colors = {
            "green": "\u001b[32;1m",
            "grey": "\u001b[38;5;240m",
            "red": "\u001b[38;5;196m",
            "yellow": "\u001b[38;5;11m",
            "purple": "\u001b[38;5;127m",
            "dark blue": "\u001b[38;5;33m",
            "cyan": "\u001b[36;1m",
            "blue": "\u001b[38;5;39m",
            "pink": "\u001b[38;5;198m",
            "gray": "\u001b[38;5;244m",
            "bright gray": "\u001b[38;5;248m",
            "reset": "\u001b[0m"
        }

        self.txt_decorations = {
            "bold": "\u001b[1m",
            "underline": "\u001b[4m",
            "reversed": "\u001b[7m"
        }

        if self.options.get("ansi", None) is None:
            self.options["ansi"] = stderr.isatty()

        if not self.options["ansi"]:
            self._clear(self.colors)
            self._clear(self.txt_decorations)

    def _clear(self, ansimap):
        for k in ansimap.keys():
            ansimap[k] = ""

    def _any_threshold(self, level):
        if self.scope != None:
            if isinstance(self.scope, list):
                for s in self.scope:
                    if s in _thresholds and _thresholds[s] <= level:
                        return True
            else:
                if self.scope in _thresholds and _thresholds[self.scope] <= level:
                    return True
        # Fallback for all
        return _thresholds[None] <= level

    def println(self, msg, out=stderr, eol="\n"):
        out.write(msg + eol)
        out.flush()

    def gray(self, text):
        gray = self.colors["gray"]
        reset = self.colors["reset"]
        return f"{gray}{text}{reset}"

    def bright_gray(self, text):
        bright_gray = self.colors["bright gray"]
        reset = self.colors["reset"]
        return f"{bright_gray}{text}{reset}"

    def bold(self, text):
        bold = self.txt_decorations["bold"]
        reset = self.colors["reset"]
        return f"{bold}{text}{reset}"

    def underline(self, text):
        underline = self.txt_decorations["underline"]
        reset = self.colors["reset"]
        return f"{underline}{text}{reset}"

    def coloured(self, color, text):
        color = self.colors[color]
        reset = self.colors["reset"]
        return f"{color}{text}{reset}"

    colored = coloured

    def reversed(self, text):
        reversed = self.txt_decorations["reversed"]
        reset = self.colors["reset"]
        return f"{reversed}{text}{reset}"

    def logger_label(self, color, icon, label):
        if self.underlined == True:
            label = self.underline(label)
        label = self.bold(label)
        label = self.coloured(color, "{} {}".format(icon, label))
        return label

    def logger(self, text="", prefix="", suffix=""):
        """New format:
        "  " [scopes] [prefix pointerSmall] type: message ["   -- " suffix]
        """
        if self.scope != None:
            if isinstance(self.scope, list):
                leader = "  " + "".join(map(lambda x: f"[{x}]", self.scope))
            else:
                leader = f"  [{self.scope}]"
        else:
            leader = " "
        if prefix != "":
            leader += f" [{prefix}] {self.figures['pointerSmall']}"
        leader = self.bright_gray(leader)
        if suffix != "":
            trailer = self.gray(f"   -- {suffix}")
        else:
            trailer = ""
        return f"{leader} {text}{trailer}"

    def log(self, text="", prefix="", suffix="", conf={}, level=INFO):
        if not self._any_threshold(level):
            return
        text = "{}:  {}".format(self.logger_label(
            conf["color"], conf["badge"], "{}".format(conf["label"])), text)
        message = self.logger(text, prefix, suffix)
        self.println(message)

    def simple(self, text="", prefix="", suffix="", level=INFO):
        if not self._any_threshold(level):
            return
        self.println(self.logger(text, prefix, suffix))

    def success(self, text="", prefix="", suffix="", level=INFO):
        if not self._any_threshold(level):
            return
        tick = self.figures["tick"]
        text = "{}:  {}".format(self.logger_label(
            "green", tick, "Success"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def start(self, text="", prefix="", suffix="", level=INFO):
        if not self._any_threshold(level):
            return
        icon = self.figures["play"]
        text = "{}:  {}".format(
            self.logger_label("green", icon, "Start"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def error(self, text="", prefix="", suffix="", level=ERROR):
        if not self._any_threshold(level):
            return
        cross = self.figures["cross"]
        text = "{}:  {}".format(self.logger_label("red", cross, "Error"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def exception(self, text="", prefix="", suffix="", level=ERROR):
        if not self._any_threshold(level):
            return
        e = exc_info()
        suffix += e[0].__name__
        if len(str(e[1])) > 0:
            suffix += e[1]
        suffix += '\n    Traceback (most recent call last):\n  ' + \
            ''.join(traceback.format_tb(e[2])).rstrip().replace('\n', '\n  ')
        self.error(text=text, prefix=prefix, suffix=suffix)

    def warning(self, text="", prefix="", suffix="", level=WARNING):
        if not self._any_threshold(level):
            return
        icon = self.figures["warning"]
        text = "{}:  {}".format(self.logger_label(
            "yellow", icon, "Warning"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    warn = warning

    def watch(self, text="", prefix="", suffix="", level=INFO):
        if not self._any_threshold(level):
            return
        icon = self.figures["ellipsis"]
        text = "{}:  {}".format(self.logger_label(
            "yellow", icon, "Watching"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def stop(self, text="", prefix="", suffix="", level=INFO):
        if not self._any_threshold(level):
            return
        icon = self.figures["squareSmallFilled"]
        text = "{}:  {}".format(self.logger_label("red", icon, "Stop"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def important(self, text="", prefix="", suffix="", level=WARNING):
        if not self._any_threshold(level):
            return
        icon = self.figures["star"]
        text = "{}:  {}".format(self.logger_label(
            "yellow", icon, "Important"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def pending(self, text="", prefix="", suffix="", level=INFO):
        if not self._any_threshold(level):
            return
        icon = self.figures["radioOff"]
        text = "{}:  {}".format(self.logger_label(
            "purple", icon, "Pending"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def debug(self, text="", prefix="", suffix="", level=DEBUG):
        if not self._any_threshold(level):
            return
        icon = self.figures["squareSmallFilled"]
        text = "{}:  {}".format(self.logger_label(
            "dark blue", icon, "Debug"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def xdebug(self, text="", prefix="", suffix="", level=XDEBUG):
        if not self._any_threshold(level):
            return
        icon = self.figures["eyes"]
        text = "{}:  {}".format(self.logger_label(
            "dark blue", icon, "XDebug"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def info(self, text="", prefix="", suffix="", level=INFO):
        if not self._any_threshold(level):
            return
        icon = self.figures["info"]
        text = "{}:  {}".format(self.logger_label("cyan", icon, "Info"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def pause(self, text="", prefix="", suffix="", level=INFO):
        if not self._any_threshold(level):
            return
        icon = self.figures["pause"]
        text = "{}:  {}".format(self.logger_label(
            "yellow", icon, "Pause"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def complete(self, text="", prefix="", suffix="", level=INFO):
        if not self._any_threshold(level):
            return
        icon = self.figures["radioOn"]
        text = "{}:  {}".format(self.logger_label(
            "blue", icon, "Complete"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def like(self, text="", prefix="", suffix="", level=INFO):
        if not self._any_threshold(level):
            return
        icon = self.figures["heart"]
        text = "{}:  {}".format(self.logger_label("pink", icon, "Like"), text)
        message = self.logger(text=text, prefix=prefix, suffix=suffix)
        self.println(message)

    def center(self, text="", prefix="", suffix=""):
        # `shutil.get_terminal_size()` actually queries stdout, not stderr;
        # nevertheless chosen for portability.
        # https://docs.python.org/3/library/shutil.html#shutil.get_terminal_size
        cols, _ = shutil.get_terminal_size()
        text = "-" * 10 + "  " + text + "  " + "-" * 10
        message = " " * ((cols - len(text)) // 2) + text
        self.println(message)

    def scoped(self, scope):
        opts = self.options
        if self.scope != None:
            if isinstance(self.scope, list):
                opts["scope"] = opts["scope"].append(scope)
                return Signale(opts)
            else:
                opts["scope"] = [self.scope, scope]
                return Signale(opts)
            return Signale()
        else:
            opts["scope"] = scope
            return Signale(opts)
        return Signale()

    def ask(self, questions=[]):
        answers = {}
        for q in questions:
            qtype = ""
            qreq = ""
            qdef = ""
            try:
                qtype = q["type"]
            except KeyError:
                qtype = "input"
            try:
                qreq = q["required"]
            except KeyError:
                qreq = False
            try:
                qdef = q["default"]
            except KeyError:
                qdef = ""
            if qtype == "input":
                if qdef == "":
                    ans = ""
                    try:
                        ans = input(self.coloured("yellow", "  ? {}: ".format(
                            q["message"])) + self.colors["cyan"])
                    except KeyboardInterrupt:
                        self.println(self.colors["reset"], out=stdout)
                        KeyboardInterrupt()
                    except EOFError:
                        self.println(self.colors["reset"], out=stdout)
                    self.println(self.colors["reset"], out=stdout, eol="")
                    if ans == "" and qreq == True:
                        while ans == "":
                            ans = self.ask([q])
                    if isinstance(ans, str):
                        answers[q["name"]] = ans
                    elif isinstance(ans, dict):
                        while isinstance(ans, dict):
                            ans = ans[q["name"]]
                        answers[q["name"]] = ans
                else:
                    ans = ""
                    try:
                        ans = input(self.coloured("yellow", "  ? {} ".format(
                            q["message"])) + self.coloured("pink", "({})".format(qdef)) + ": " + self.colors["cyan"])
                    except KeyboardInterrupt:
                        self.println(self.colors["reset"], out=stdout)
                        KeyboardInterrupt()
                    except EOFError:
                        self.println(self.colors["reset"], out=stdout)
                    self.println(self.colors["reset"], out=stdout, eol="")
                    if ans == "":
                        ans = qdef
                    if isinstance(ans, str):
                        answers[q["name"]] = ans
                    elif isinstance(ans, dict):
                        while isinstance(ans, dict):
                            ans = ans[q["name"]]
                        answers[q["name"]] = ans
        return answers


if __name__ == "__main__":
    def _stacktrace_test():
        raise KeyError

    s = Signale({
        "underlined": False
    })
    s.center("Testing Logger")
    s.simple("ABC", prefix="Debugger", suffix="xyz")
    s.info("Starting", prefix="Debugger")
    s.success("Started Successfully", prefix="Debugger", suffix="xyz")
    s.watch("Watching All Files", prefix="Debugger")
    s.error("Something Went Wrong", prefix="Debugger")
    s.warning("Deprecation Warning", prefix="Debugger")
    s.pending("Postponed", prefix="Debugger")
    s.debug("Found A Bug on L55", prefix="Debugger")
    s.xdebug("Let's See Where This Is Going", prefix="Debugger")
    s.start("Started New Process", prefix="Debugger")
    s.pause("Process Paused", prefix="Debugger")
    s.complete("Task Completed", prefix="Debugger")
    s.important("New Update Available. Please Update!", prefix="Debugger")
    s.like("I Love Signale", prefix="Debugger")
    s.stop("Stopping", prefix="Debugger")
    try:
        _stacktrace_test()
    except Exception:
        s.exception("Exception output")

    s.println("\n")

    s = Signale({
        "ansi": False
    })
    s.center("Testing Logger without colors")
    s.simple("ABC", prefix="Debugger", suffix="xyz")
    s.warn("Alternate Warning", prefix="Debugger")

    s.println("\n")

    logger = Signale({
        "scope": ""
    })
    logger.success("Started Successfully", prefix="Debugger")
    logger.warning("`a` function is deprecated", suffix="main.py")
    logger.complete("Run Complete")

    logger.println("\n")

    logger = Signale({"scope": "custom"})
    logger.success("Started Successfully", prefix="Debugger")
    logger.warning("`a` function is deprecated", suffix="main.py")
    logger.complete("Run Complete")

    logger = Signale({
        "scope": "global scope",
        "custom": [
            {
                "badge": "!",
                "label": "Attention",
                "color": "red",
                "name": "attention",
                "level": WARNING,
            }
        ],
        "underlined": True
    })

    logger2 = logger.scoped("inner")

    logger.attention("It Works!")  # pylint: disable=E1101
    logger2.attention("With Logger2")  # pylint: disable=E1101

    logger = Signale()
    ans = logger.ask([
        {
            "type": "input",
            "name": "username",
            "message": "Your Name",
            "default": "Shardul"
        }
    ])

    logger.println(logger.bold(logger.coloured("pink", ans)))

    logger.println("\n")

    logger.println(logger.bold("Bold Text"))
    logger.println(logger.underline("Underlined"))
    logger.println(logger.reversed("Reversed"))

    logger = Signale()  # Option can be passed to the constructor
    logger.info("Signale.py is amazing", prefix="Logger")

    logger = Signale({
        "scope": "global scope",
        "custom": [
            {
                "badge": "!",
                "label": "Attention",
                "color": "red",
                "name": "attention",
                "level": WARNING,
            }
        ],
        "underlined": False
    })

    logger.attention("It Works!")  # pylint: disable=E1101
    logger.scoped("inner").attention(  # pylint: disable=E1101
        "Salute Signale.py")

    logger.println("\n")
    logger.center("Playing With Levels And Thresholds")
    set_threshold(None, 'WARNING')
    logger.debug("Should Not Be Visible")
    logger.warning("Should Be Visible")

    set_threshold("global scope", DEBUG)
    logger.debug("Now Visible")
    logger.xdebug("Invisible")
    logger2.xdebug("Invisible as well")

    set_threshold("inner", XDEBUG)
    logger2.xdebug("Now Visible")
