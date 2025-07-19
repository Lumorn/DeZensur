import de from '../i18n/de.json';
import en from '../i18n/en.json';

test('de.json und en.json besitzen identische Keys', () => {
  const keysDe = Object.keys(de).sort();
  const keysEn = Object.keys(en).sort();
  expect(keysDe).toEqual(keysEn);
  expect(keysDe).toMatchSnapshot();
});
