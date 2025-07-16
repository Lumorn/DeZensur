class StableDiffusionInpaintPipeline:
    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        return cls()

    def to(self, device):
        return self

    def __call__(self, prompt="", negative_prompt="", image=None, mask_image=None, num_inference_steps=30, strength=0.98):
        from tests.PIL import Image
        return type('Result', (), {'images': [Image.new('RGB', image.size)]})
