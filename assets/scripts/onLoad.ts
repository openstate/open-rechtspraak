import {Tooltip} from 'bootstrap';


import {config, library, dom} from '@fortawesome/fontawesome-svg-core'
import {far} from '@fortawesome/free-regular-svg-icons'
import {faTwitter, faLinkedin, faFacebook, faGithub} from '@fortawesome/free-brands-svg-icons'

const initFontawesome = () => {
  config.autoAddCss = false
  library.add(far, faTwitter, faLinkedin, faFacebook, faGithub)
  dom.watch()
}

const initTooltips = () => {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new Tooltip(tooltipTriggerEl)
  })
}
window.addEventListener('load', (event) => {
  initTooltips();
  initFontawesome();
})
