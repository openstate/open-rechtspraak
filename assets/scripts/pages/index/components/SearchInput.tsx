import React, { useEffect, useState } from 'react';
import { useDebounce } from 'use-debounce';

interface Props {
  setQuery: (q: string) => void
};


function SearchInput({ setQuery }: Props) {
  const [text, setText] = useState("");
  const [debounced] = useDebounce(text, 200);

  useEffect(() => {
    setQuery(debounced);
  }, [debounced, setQuery]);

  return (
    <div>
      <input
        className="form-control"
        placeholder="Zoek op naam, bijvoorbeeld 'De Jong'"
        onChange={(e) => {
          setText(e.target.value);
        }}
      />
    </div>
  );
}

export default SearchInput;
