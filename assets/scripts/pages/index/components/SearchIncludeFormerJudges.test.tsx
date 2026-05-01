import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import SearchIncludeFormerJudges from './SearchIncludeFormerJudges';

const setup = () => {
  jest.useFakeTimers();
  const callback = jest.fn((value: boolean) => value);
  const element = render(<SearchIncludeFormerJudges setIncludeFormerJudges={callback} />);
  const input = screen.getByLabelText("Zoek ook door oud-functionarissen") as HTMLInputElement;

  return {
    input, element, callback,
  };
};

it('renders an input field', () => {
  const { input } = setup();
  expect(input).toBeVisible();
});

it('can be clicked on to toggle a value', async () => {
  const { input } = setup();

  await waitFor(() => expect(input.checked).toBe(false), { timeout: 1000 });
  userEvent.click(input);
  await waitFor(() => expect(input.checked).toBe(true), { timeout: 1000 });
});

it('the callback is called when entering an input', async () => {
  const { input, callback } = setup();

  userEvent.click(input);

  await waitFor(() => expect(callback).toHaveBeenCalledWith(true), { timeout: 1000 });
  expect(callback).toHaveBeenCalledTimes(2);
});
