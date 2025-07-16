class DummyModel:
    def __init__(self, checkpoint=None):
        self.ckpt = checkpoint
        self.device = "cpu"

    def to(self, device):
        self.device = device

class SamPredictor:
    def __init__(self, model):
        self.model = model
        self.image_shape = (0, 0)

    def set_image(self, image):
        # Ermittelt Bildgröße aus einer Liste oder nutzt Fallback
        try:
            h = len(image)
            w = len(image[0]) if h else 0
        except Exception:
            h, w = 10, 10
        self.image_shape = (h, w)

    def predict(self, **kwargs):
        h, w = self.image_shape
        mask = [[True for _ in range(w)] for _ in range(h)]
        return [mask], None, None

def _factory(checkpoint=None):
    return DummyModel(checkpoint)

sam_model_registry = {"vit_h": _factory, "vit_t": _factory}
