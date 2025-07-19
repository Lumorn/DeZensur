import { test, expect } from '@playwright/test';

test('SidePanel zeigt Bild-Eigenschaften an', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.evaluate(() => {
    window.dialogs = { openImages: async () => ['/tmp/test.png'] } as any;
  });
  await page.keyboard.press('Control+O');
  // Thumbnail auswählen
  await page.locator('button >> nth=0').click();
  await expect(page.getByTestId('img-props')).toBeVisible();
});
