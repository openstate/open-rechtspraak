import React from 'react';

type Props = {
  count: number
};

function SearchCounter({ count }: Props) {
  return (
    <p>
      <span id="search-results-count">{(count !== undefined) ? count : '____'}</span>
      {' '}
      personen gevonden
    </p>
  );
}

export default SearchCounter;
