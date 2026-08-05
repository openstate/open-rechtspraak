import { config, dom, library } from '@fortawesome/fontawesome-svg-core';
import {
  faMastodon, faBluesky, faLinkedin, faGithub,
} from '@fortawesome/free-brands-svg-icons';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { Tooltip } from 'bootstrap';

const initFontawesome = () => {
  config.autoAddCss = false;
  library.add(fas, faMastodon, faBluesky, faLinkedin, faGithub);
  dom.watch();
};

const initTooltips = () => {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map((tooltipTriggerEl) => new Tooltip(tooltipTriggerEl));
};

window.addEventListener('load', () => {
  initTooltips();
  initFontawesome();
});
