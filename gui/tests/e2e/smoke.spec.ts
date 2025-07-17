import { test, expect } from '@playwright/test';

// Einfacher Smoke-Test für Import und Inpaint
// Aktuell nur ein Platzhalter, da die IPC-Logik noch fehlt

test('Import > Detect > Inpaint > Export', async ({ page }) => {
  await page.goto('http://localhost:5173');
  expect(page).toBeTruthy();
});
