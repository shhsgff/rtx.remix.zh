"""Runtime translation engine for omni.ui widget trees."""
import json
import os
import time

import carb
import omni.kit.app
import omni.ui as ui

_DEBUG_LOG = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
    "rtx-remix-zh.log",
)


class TranslationEngine:
    """Walks omni.ui windows periodically and rewrites known English texts to Chinese."""

    SCAN_EVERY_N_FRAMES = 120  # ~2 scans/sec at 60fps foreground; keeps full-tree walks from hogging the UI loop

    def __init__(self, dict_path):
        with open(dict_path, "r", encoding="utf-8") as fh:
            self._dict = json.load(fh)
        self._known_originals = {}  # id(widget) -> original English text
        self._missed = set()        # English texts not in dictionary (for iterating)
        self._missed_dumped = False
        self._tick = 0
        self._sub = None
        self._log(f"dictionary loaded: {len(self._dict)} entries")

    # ---------------------------------------------------------------- lifecycle
    def start(self):
        app = omni.kit.app.get_app()
        self._sub = app.get_update_event_stream().create_subscription_to_pop(
            self._on_update, name="rtx.remix.zh scan"
        )

    def stop(self):
        self.dump_missed()
        self._sub = None

    def _on_update(self, e, *args, **kwargs):
        self._tick += 1
        if self._tick % self.SCAN_EVERY_N_FRAMES:
            return
        try:
            self.scan()
        except Exception as exc:  # defensive: never break the app loop
            carb.log_warn(f"[rtx.remix.zh] scan error: {exc}")

    # ---------------------------------------------------------------- scanning
    def scan(self):
        # get_windows() returns a mix of ui.Window / ui.ToolBar / WindowHandle.
        # Only Window and ToolBar expose .frame (the widget tree root).
        try:
            windows = ui.Workspace.get_windows()
        except Exception:
            return
        for handle in windows:
            if not isinstance(handle, (ui.Window, ui.ToolBar)):
                continue
            try:
                frame = handle.frame
            except Exception:
                continue
            self._walk(frame)
        if not self._missed_dumped:
            self._missed_dumped = True
            self.dump_missed()

    def _walk(self, root):
        # Iterative DFS to avoid deep-recursion limits on big widget trees.
        stack = [root]
        while stack:
            widget = stack.pop()
            if widget is None:
                continue
            self._translate(widget)
            try:
                stack.extend(ui.Inspector.get_children(widget))
            except Exception:
                pass

    def _translate(self, widget):
        try:
            text = widget.text
        except Exception:
            return
        if not isinstance(text, str) or not text or not text.isprintable():
            return
        key = id(widget)
        original = self._known_originals.get(key)
        if original is not None:
            # Already known widget: re-apply if the framework reset it to English.
            if text == original:
                self._apply(widget, original)
            return
        if text in self._dict:
            self._known_originals[key] = text
            self._apply(widget, text)
        elif len(self._missed) < 2000:
            self._missed.add(text)

    def _apply(self, widget, english):
        zh = self._dict[english]
        if zh == english:
            return
        try:
            widget.text = zh
        except Exception as exc:
            carb.log_warn(f"[rtx.remix.zh] cannot set text for {english!r}: {exc}")

    # ---------------------------------------------------------------- debug
    def dump_missed(self):
        if not self._missed:
            return
        lines = ["--- untranslated texts (for dictionary iteration) ---"]
        lines.extend(sorted(self._missed))
        self._log("\n".join(lines))

    def _log(self, message):
        try:
            with open(_DEBUG_LOG, "a", encoding="utf-8") as fh:
                fh.write(f"[{time.strftime('%H:%M:%S')}] {message}\n")
        except Exception:
            pass
        carb.log_info(f"[rtx.remix.zh] {message}")
