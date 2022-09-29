import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import React from 'react';

import SearchInput from './SearchInput';

const setup = () => {
  jest.useFakeTimers();
  const callback = jest.fn((value: string) => value);
  const element = render(<SearchInput setQuery={callback} />);
  const input = screen.getByPlaceholderText("Zoek op naam, bijvoorbeeld 'De Jong'") as HTMLInputElement;

  return {
    input, element, callback,
  };
};

it('renders an input field', () => {
  const { input } = setup();
  expect(input).toBeTruthy();
});

it('can enter a value in the input field', async () => {
  const { input } = setup();
  const inputValue = 'De Jong';

  userEvent.type(input, inputValue);
  await waitFor(() => expect(input.value).toBe(inputValue), { timeout: 1000 });
});

it('the callback is called when entering an input', async () => {
  const { input, callback } = setup();
  const inputValue = 'De Jong';

  userEvent.type(input, inputValue);

  // Callback is debounced, hence we first assert that it isn't called
  // but subsequently assert that it's called within a second
  expect(callback).not.toHaveBeenCalledWith(inputValue);
  await waitFor(() => expect(callback).toHaveBeenCalledWith(inputValue), { timeout: 1000 });
  expect(callback).toBeCalledTimes(1);
});
