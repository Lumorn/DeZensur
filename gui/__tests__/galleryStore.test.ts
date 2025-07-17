import { useGalleryStore } from '../src/renderer/stores/useGalleryStore';

describe('addImages', () => {
  beforeEach(() => {
    useGalleryStore.setState({ images: [], selectedId: null });
  });

  test('fügt eindeutige IDs hinzu und ignoriert Duplikate', () => {
    useGalleryStore.getState().addImages(['/a.png', '/b.png', '/a.png']);
    const images = useGalleryStore.getState().images;
    expect(images).toHaveLength(2);
    expect(images[0].id).not.toBe(images[1].id);
  });
});
