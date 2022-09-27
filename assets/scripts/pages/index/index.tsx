import useAxios from 'axios-hooks';
import React, { useEffect, useState } from 'react';

import ErrorMessage from '../../components/ErrorMessage';
import { Person } from '../../types';
import registerComponent from '../../utils/registerComponent';
import SearchCounter from './components/SearchCounter';
import SearchInput from './components/SearchInput';
import SearchResultRow from './components/SearchResultRow';

function Search() {
  const [q, setQuery] = useState<string>('');
  const [{ data, loading, error }, refetch] = useAxios({ url: 'api/v1/person' }, { manual: true });

  useEffect(() => {
    refetch({
      params: {
        q,
        limit: 100,
      },
    });
  }, [q]);

  return (
    <div>
      <SearchInput setQuery={setQuery} />
      <SearchCounter count={data?.count} />
      {error && <ErrorMessage />}

      {loading && (
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Laden...</span>
        </div>
      )}

      {data?.data.length > 0 && (
        data.data.map((person: Person) => <SearchResultRow key={person.id} {...person} />)
      )}
    </div>
  );
}

registerComponent(<Search />, 'search');
