import { test, expect } from '@playwright/test';

test('Bilder werden über Shortcut hinzugefügt', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.evaluate(() => {
    window.dialogs = { openImages: async () => ['/tmp/1.png', '/tmp/2.png'] } as any;
  });
  await page.keyboard.press('Control+O');
  const thumbs = page.locator('img');
  await expect(thumbs).toHaveCount(2);
});
