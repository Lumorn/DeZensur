import { test, expect } from '@playwright/test';

// Testet das Öffnen des Masken-Editors über die Vorschau

test('Maskeneditor öffnet sich und zeigt Buttons', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.evaluate(() => {
    window.dialogs = { openImages: async () => ['/tmp/edit.png'] } as any;
  });
  await page.keyboard.press('Control+O');
  await page.getByText('Maske editieren').click();
  await expect(page.getByText('Abbrechen')).toBeVisible();
  await expect(page.getByText('Speichern')).toBeVisible();
});
