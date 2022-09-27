import React from 'react';

import { Person, ProfessionalDetail } from '../../../types';

type ProfessionalDetailPillProps = {
  value: string
  variant?: string
};

function ProfessionalDetailPill({ value, variant = 'primary' }: ProfessionalDetailPillProps) {
  return (
    <span className={`badge rounded-pill bg-${variant} ms-2`}>
      {value}
    </span>
  );
}

function SearchResultRow({ id, toon_naam, beroepsgegevens }: Person) {
  return (
    <a className="search-result-person" href={`person/${id}`}>
      <div className="card mb-3">
        <div className="card-body">
          <h3 className="search-result-person__name">{toon_naam}</h3>
          {beroepsgegevens.length > 0 && <h4 className="text-secondary">{beroepsgegevens[0]?.function}</h4>}
        </div>

        <div className="card-footer">
          {beroepsgegevens.map((professionalDetail: ProfessionalDetail) => (
            <React.Fragment key={professionalDetail.id}>
              <ProfessionalDetailPill
                key={`org-${professionalDetail.id}`}
                value={professionalDetail.organisation}
                variant="primary"
              />
              <ProfessionalDetailPill
                key={`func-${professionalDetail.id}`}
                value={professionalDetail.function}
                variant="secondary"
              />
            </React.Fragment>
          ))}
        </div>
      </div>
    </a>
  );
}

export default SearchResultRow;
