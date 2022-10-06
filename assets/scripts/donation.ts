import { Modal } from 'bootstrap';

const lastMonth = (): Date => {
  const date = new Date();
  date.setMonth(date.getMonth() - 1);
  return date;
};

class DonationUser {
  STORAGE_KEY = 'last-donation-modal-shown-at';

  store(value: any): void {
    localStorage.setItem(this.STORAGE_KEY, value);
  }

  registerModalShown(): void {
    const date = new Date();
    this.store(date);
  }

  lastTimeModalShown(): (Date | null) {
    const value = localStorage.getItem(this.STORAGE_KEY);

    if (value === null) {
      return null;
    }

    return new Date(value);
  }

  modalNeverShown(): boolean {
    return this.lastTimeModalShown() === null;
  }

  modalShownInLastMonth(): boolean {
    const lastTimeModalShown = this.lastTimeModalShown();

    if (lastTimeModalShown === null) {
      return false;
    }

    return lastTimeModalShown < lastMonth();
  }

  shouldShowModal(): boolean {
    /* Show a modal if either:
      1. a donation modal was never shown, or
      2. the last modal was shown over a month ago
    */
    return this.modalNeverShown() || this.modalShownInLastMonth();
  }
}

const initDonationModal = () => {
  const user = new DonationUser();
  const modal = new Modal('#donationModal');

  if (user.shouldShowModal()) {
    modal.show();
    user.registerModalShown();
  }
};

// Only initialize modal logic after 5 seconds to prevent an annoying popup on first visit
setTimeout(initDonationModal, 5000);
