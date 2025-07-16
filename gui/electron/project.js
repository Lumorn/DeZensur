// Verwaltet das Projekt im Hauptprozess
import { ipcMain } from 'electron';
import fs from 'fs';
import path from 'path';

class Project {
  constructor(root) {
    this.root = root;
    this.file = root + '.dezproj';
    this.data = {
      schema: 1,
      title: path.basename(root),
      created: new Date().toISOString(),
      images: [],
      settings: {},
    };
  }

  static load(projFile) {
    const txt = fs.readFileSync(projFile, 'utf-8');
    const data = JSON.parse(txt);
    const p = new Project(projFile.replace(/\.dezproj$/, ''));
    p.data = data;
    return p;
  }

  save() {
    fs.writeFileSync(this.file, JSON.stringify(this.data, null, 2));
  }

  ensureDirs() {
    ['originals', 'masks', 'processed', 'logs'].forEach((d) => {
      fs.mkdirSync(path.join(this.root, d), { recursive: true });
    });
  }

  addImages(paths) {
    this.ensureDirs();
    paths.forEach((p) => {
      const dest = path.join(this.root, 'originals', path.basename(p));
      fs.copyFileSync(p, dest);
      this.data.images.push({
        id: path.parse(dest).name,
        file: path.relative(this.root, dest),
        status: 'pending',
      });
    });
    this.save();
  }
}

let project = null;

export function ProjectIPC(ipc) {
  ipc.handle('project:new', (_e, root) => {
    project = new Project(root);
    project.save();
    return { ...project.data, root: project.root };
  });
  ipc.handle('project:open', (_e, file) => {
    project = Project.load(file);
    return { ...project.data, root: project.root };
  });
  ipc.handle('project:save', () => {
    project?.save();
    return true;
  });
  ipc.handle('project:addImages', (_e, paths) => {
    project?.addImages(paths);
    return project ? { ...project.data, root: project.root } : null;
  });
  ipc.handle('backend:call', async (_e, endpoint, payload) => {
    const res = await fetch('http://127.0.0.1:8787' + endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  });
}
