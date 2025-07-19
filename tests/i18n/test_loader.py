from core import i18n


def test_load_translations() -> None:
    de = i18n.load_translations("de")
    en = i18n.load_translations("en")
    assert de.get("file") == "Datei"
    assert en.get("add_images") == "Add Images…"

