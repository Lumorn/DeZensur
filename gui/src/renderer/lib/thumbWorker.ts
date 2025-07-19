self.onmessage = async (e) => {
  const { id, path } = e.data;
  try {
    const res = await fetch(path);
    const blob = await res.blob();
    const img = await createImageBitmap(blob);
    const size = 160;
    const canvas = new OffscreenCanvas(size, size);
    const ctx = canvas.getContext('2d');
    const scale = Math.min(size / img.width, size / img.height);
    const w = img.width * scale;
    const h = img.height * scale;
    ctx.drawImage(img, 0, 0, w, h);
    const outBlob = await canvas.convertToBlob();
    const reader = new FileReader();
    reader.onload = () => {
      self.postMessage({ id, thumb: reader.result });
    };
    reader.readAsDataURL(outBlob);
  } catch {
    self.postMessage({ id, thumb: path });
  }
};
