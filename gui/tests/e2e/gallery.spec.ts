import { test, expect } from '@playwright/test';

test('Drag & Drop Import fügt Bilder hinzu', async ({ page }) => {
  await page.goto('http://localhost:5173');
  const dt = await page.evaluateHandle(() => {
    const d = new DataTransfer();
    const f = new File([''], 'drop.png');
    Object.defineProperty(f, 'path', { value: '/tmp/drop.png' });
    d.items.add(f);
    return d;
  });
  await page.dispatchEvent('[data-testid="gallery"]', 'dragover', { dataTransfer: dt });
  await page.dispatchEvent('[data-testid="gallery"]', 'drop', { dataTransfer: dt });
  const thumbs = page.locator('img');
  await expect(thumbs).toHaveCount(1);
});
