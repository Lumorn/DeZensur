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

  test('erzeugt Thumbnails im Worker', (done) => {
    // Einfache Worker-Attrappe, die sofort eine Data-URL zurückgibt
    // @ts-ignore
    global.Worker = class {
      onmessage = null;
      postMessage(data) {
        this.onmessage({ data: { id: data.id, thumb: 'data:test' } });
      }
    };
    useGalleryStore.getState().addImages(['/c.png']);
    setTimeout(() => {
      const img = useGalleryStore.getState().images[0];
      expect(img.thumb).toBe('data:test');
      done();
    }, 0);
  });
});
