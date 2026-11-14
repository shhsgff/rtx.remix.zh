"""RTX Remix Chinese (zh-CN) translation extension.

Translates static UI texts of NVIDIA RTX Remix Toolkit at runtime by walking
the omni.ui widget tree and rewriting widget.text with a JSON dictionary.
"""
__all__ = ["RTXRemixZhExtension"]

import os

import carb
import omni.ext
import omni.kit.app

from .translator import TranslationEngine


class RTXRemixZhExtension(omni.ext.IExt):
    """Extension entry point. Hooks the app update stream and runs the translator."""

    def on_startup(self, ext_id):
        carb.log_info("[rtx.remix.zh] on_startup")
        dict_path = self._find_dictionary(ext_id)
        if not dict_path or not os.path.isfile(dict_path):
            carb.log_error(f"[rtx.remix.zh] dictionary not found: {dict_path}")
            return
        self._engine = TranslationEngine(dict_path)
        self._engine.start()
        carb.log_info(f"[rtx.remix.zh] engine started, dict={dict_path}")

    def on_shutdown(self):
        carb.log_info("[rtx.remix.zh] on_shutdown")
        engine = getattr(self, "_engine", None)
        if engine is not None:
            engine.stop()

    @staticmethod
    def _find_dictionary(ext_id):
        # Preferred: ask the extension manager for the extension folder.
        try:
            mgr = omni.kit.app.get_app().get_extension_manager()
            path = mgr.get_extension_path(ext_id)
            if path:
                return os.path.join(path, "data", "zh-CN.json")
        except Exception:
            pass
        # Fallback: walk up from this file: .../exts/rtx.remix.zh/rtx/remix/zh/__init__.py
        d = os.path.dirname(os.path.abspath(__file__))
        for _ in range(4):
            d = os.path.dirname(d)
        return os.path.join(d, "data", "zh-CN.json")
