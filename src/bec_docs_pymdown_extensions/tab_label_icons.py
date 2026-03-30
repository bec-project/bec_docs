import importlib
import re
from pathlib import Path
from urllib.parse import quote

from markdown.extensions import Extension

_TAB_ICON_RE = re.compile(r"^\s*:(?P<icon>[a-z0-9-]+):\s*")
_ICON_CACHE: dict[str, str | None] = {}
_PATCHED_TAB_BLOCK = False


def _resolve_icon_path(icon_name: str) -> Path | None:
    if icon_name.startswith("material-"):
        return _icon_root() / "material" / f"{icon_name.removeprefix('material-')}.svg"
    if icon_name.startswith("fontawesome-brands-"):
        return _icon_root() / "fontawesome" / "brands" / f"{icon_name.removeprefix('fontawesome-brands-')}.svg"
    if icon_name.startswith("fontawesome-solid-"):
        return _icon_root() / "fontawesome" / "solid" / f"{icon_name.removeprefix('fontawesome-solid-')}.svg"
    return None


def _icon_root() -> Path:
    zensical_path = Path(importlib.import_module("zensical").__file__).resolve().parent
    return zensical_path / "templates" / ".icons"


def _load_svg(icon_name: str) -> str | None:
    if icon_name not in _ICON_CACHE:
        icon_path = _resolve_icon_path(icon_name)
        if icon_path is None or not icon_path.exists():
            _ICON_CACHE[icon_name] = None
        else:
            _ICON_CACHE[icon_name] = icon_path.read_text()
    return _ICON_CACHE[icon_name]


def _load_svg_data_url(icon_name: str) -> str | None:
    svg = _load_svg(icon_name)
    if svg is None:
        return None
    return f"url(\"data:image/svg+xml;utf8,{quote(svg)}\")"


def _apply_icon_shortcode_to_label(label) -> None:
    text = label.text or ""
    match = _TAB_ICON_RE.match(text)
    if not match:
        return

    icon_data_url = _load_svg_data_url(match.group("icon"))
    if not icon_data_url:
        return

    label.text = text[match.end() :]
    label.attrib["data-tab-icon"] = "true"

    style = label.attrib.get("style", "")
    if style and not style.endswith(";"):
        style += ";"
    style += f"--bec-tab-icon: {icon_data_url};"
    label.attrib["style"] = style


def _patch_pymdownx_tab_block() -> None:
    global _PATCHED_TAB_BLOCK
    if _PATCHED_TAB_BLOCK:
        return

    pymdownx_tab = importlib.import_module("pymdownx.blocks.tab")
    original_on_create = pymdownx_tab.Tab.on_create

    def wrapped_on_create(self, parent):
        tab_group = original_on_create(self, parent)
        if self.alternate_style:
            label_containers = [
                d for d in tab_group.findall("div") if d.attrib.get("class") == "tabbed-labels"
            ]
            if not label_containers:
                return tab_group
            labels = label_containers[0].findall("label")
        else:
            labels = tab_group.findall("label")

        if labels:
            _apply_icon_shortcode_to_label(labels[-1])
        return tab_group

    pymdownx_tab.Tab.on_create = wrapped_on_create
    _PATCHED_TAB_BLOCK = True


class TabLabelIcons(Extension):
    def extendMarkdown(self, md):
        _patch_pymdownx_tab_block()


def make_extension(**kwargs):
    return TabLabelIcons(**kwargs)
