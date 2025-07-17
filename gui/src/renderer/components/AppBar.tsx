import React from 'react';

// Oberste App-Bar mit Logo und Menüs
export default function AppBar() {
  return (
    <header className="h-15 flex items-center px-4 bg-[#1e1e2f] text-white">
      <h1 className="font-semibold mr-auto">DeZensur</h1>
      <nav className="space-x-4 hidden md:block">
        <button className="hover:underline">File</button>
        <button className="hover:underline">Edit</button>
        <button className="hover:underline">View</button>
        <button className="hover:underline">Help</button>
      </nav>
      <div className="ml-auto flex space-x-2">
        <button aria-label="Settings">⚙</button>
        <button aria-label="GPU-Status">🖥</button>
        <button aria-label="Working-Dir">📁</button>
      </div>
    </header>
  );
}
