from core.prompt_helper import BASE_PROMPT, NEG_PROMPT, build_prompt


def test_tags_added():
    p, n = build_prompt(["penis", "nipple_f"], "")
    assert "penis" in p and "nipples" in p
    assert p.startswith(BASE_PROMPT)
    assert n == NEG_PROMPT
