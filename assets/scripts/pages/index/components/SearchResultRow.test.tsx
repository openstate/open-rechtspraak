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

it('renders all professional details', () => {
  render(<SearchResultRow {...PERSON_FIXTURE} />);

  PERSON_FIXTURE.professional_details.forEach((item: ProfessionalDetail) => {
    screen.getAllByText(item.function).forEach((element) => expect(element).toBeVisible());
    screen.getAllByText(item.organisation).forEach((element) => expect(element).toBeVisible());
  });
});

it('renders a clickable element', async () => {
  render(<SearchResultRow {...PERSON_FIXTURE} />);
  const url = personUrl(PERSON_FIXTURE.id);

  expect(screen.getByText(PERSON_FIXTURE.toon_naam).closest('a')).toHaveAttribute('href', url);
});
