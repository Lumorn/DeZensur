"""
Hilfsfunktionen zum Zusammen­bauen des Inpainting-Prompts.
"""
from typing import List

BASE_PROMPT = "masterpiece, best quality, anime illustration, detailed anatomy, soft shading"
NEG_PROMPT  = "lowres, blurry, bad anatomy, extra limbs, mosaic, censor bar"

TAG_MAP = {
    "penis":  ["penis, testicles, uncensored, detailed skin, veins"],
    "pussy":  ["vagina, uncensored, labia, detailed skin"],
    "nipple_f": ["nude, bare breasts, nipples, uncensored"],
}

def build_prompt(labels: List[str], user_prompt: str | None) -> tuple[str,str]:
    """
    Gibt (prompt, negative_prompt) zurück.
    - labels  : Liste aus Censor-Detector (z.B. ["penis"])
    - user_prompt : Freitext aus GUI (optional, kann '' sein)
    """
    extra = []
    for lab in labels:
        extra.extend(TAG_MAP.get(lab, []))
    prompt = BASE_PROMPT
    if extra:
        prompt += ", " + ", ".join(extra)
    if user_prompt:
        prompt += ", " + user_prompt.strip()
    return prompt, NEG_PROMPT
