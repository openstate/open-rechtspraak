import {Modal} from 'bootstrap';

class DonationUser {
  STORAGE_KEY = 'last-donation-modal-shown-at';

  store(value) {
    localStorage.setItem(this.STORAGE_KEY, value);
  }

  registerModalShown() {
    const date = new Date()
    this.store(date)
  }

  lastTimeModalShown() {
    let value = localStorage.getItem(this.STORAGE_KEY);
    return value === null ? null : Date.parse(value);
  }

  modalNeverShown() {
    return this.lastTimeModalShown() === null;
  }

  lastMonth() {
    const date = new Date();
    date.setMonth(date.getMonth() - 1);
    return date
  }

  modalShownInLastMonth() {
    return this.lastTimeModalShown() < this.lastMonth()
  }

  shouldShowModal() {
    /* Show a modal if either:
      1. a donation modal was never shown, or
      2. the last modal was shown over a month ago
    */
    return this.modalNeverShown() || this.modalShownInLastMonth();
  }
}


const initDonationModal = () => {
  const user = new DonationUser()
  const modal = new Modal('#donationModal')

  modal.show();
  if (user.shouldShowModal()) {
    user.registerModalShown();
  }
}

// Only initialize modal logic after 5 seconds to prevent an annoying popup on first visit
setTimeout(initDonationModal, 50)
