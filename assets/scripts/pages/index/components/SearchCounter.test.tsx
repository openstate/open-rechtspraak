import { render, screen } from '@testing-library/react';
import React from 'react';

import { randRange } from '../../../utils/math';
import SearchCounter from './SearchCounter';

it('renders the count prop', () => {
  const count = randRange(0, 1000);
  render(<SearchCounter count={count} />);
  expect(screen.getByText(count)).toBeTruthy();
});
