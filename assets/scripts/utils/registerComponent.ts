import { ReactNode } from 'react';
import { createRoot } from 'react-dom/client';

export default function registerComponent(component: ReactNode, domId: string) {
  const el = document.getElementById(domId);
  if (el) {
    const root = createRoot(el);
    root.render(component);
  }
}
