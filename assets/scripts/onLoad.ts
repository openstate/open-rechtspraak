import { config, dom, library } from '@fortawesome/fontawesome-svg-core';
import {
  faFacebook, faGithub,
  faLinkedin, faTwitter,
} from '@fortawesome/free-brands-svg-icons';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { Tooltip } from 'bootstrap';

const initFontawesome = () => {
  config.autoAddCss = false;
  library.add(fas, faTwitter, faLinkedin, faFacebook, faGithub);
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
