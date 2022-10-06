import React from 'react';
import { DebounceInput } from 'react-debounce-input';

type Props = {
  setQuery: (q: string) => void
};

function SearchInput({ setQuery }: Props) {
  return (
    <DebounceInput
      minLength={1}
      debounceTimeout={200}
      placeholder="Zoek op naam, bijvoorbeeld 'De Jong'"
      className="form-control"
      onChange={(e) => setQuery(e.target.value)}
    />
  );
}

export default SearchInput;
