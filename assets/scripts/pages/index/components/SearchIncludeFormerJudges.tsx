import React, { useEffect, useState } from 'react';
import { useDebounce } from 'use-debounce';

interface Props {
  setIncludeFormerJudges: (value: boolean) => void
};


function SearchIncludeFormerJudges({ setIncludeFormerJudges }: Props) {
  const [value, setValue] = useState(false);

  useEffect(() => {
    setIncludeFormerJudges(value);
  }, [value]);

  return (
    <div className="form-check form-switch">
      <input className="form-check-input" type="checkbox" role="switch" id="includeFormerJudges"
        onChange={(e) => {
          setValue(!value);
        }}
        checked={value}
      />
      <label className="form-check-label" htmlFor="includeFormerJudges">Zoek ook door oud-functionarissen</label>
    </div>
  );
}

export default SearchIncludeFormerJudges;
