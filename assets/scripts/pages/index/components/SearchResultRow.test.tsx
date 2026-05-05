import { render, screen } from '@testing-library/react';
import React from 'react';

import { PERSON_FIXTURE } from '../../../factories';
import { ProfessionalDetail } from '../../../types';
import { personUrl } from '../../../urls';
import SearchResultRow from './SearchResultRow';

it('renders name of the person', () => {
  render(<SearchResultRow {...PERSON_FIXTURE} />);
  expect(screen.getByText(PERSON_FIXTURE.toon_naam)).toBeVisible();
});

it('renders professional details without an end date', () => {
  render(<SearchResultRow {...PERSON_FIXTURE} />);

  PERSON_FIXTURE.professional_details.forEach((item: ProfessionalDetail) => {
    if (item.end_date === null) {
      screen.getAllByText(item.function).forEach((element) => expect(element).toBeVisible());
      screen.getAllByText(item.organisation).forEach((element) => expect(element).toBeVisible());
    }
  });
});

it('does not render professional details with an end date', () => {
  render(<SearchResultRow {...PERSON_FIXTURE} />);

  PERSON_FIXTURE.professional_details.forEach((item: ProfessionalDetail) => {
    if (item.end_date !== null) {
      expect(screen.queryByText(item.function)).toBeNull()
      expect(screen.queryByText(item.organisation)).toBeNull()
    }
  });
});


it('renders a clickable element', async () => {
  render(<SearchResultRow {...PERSON_FIXTURE} />);
  const url = personUrl(PERSON_FIXTURE.id);

  expect(screen.getByText(PERSON_FIXTURE.toon_naam).closest('a')).toHaveAttribute('href', url);
});
