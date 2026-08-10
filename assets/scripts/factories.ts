import { Person, ProfessionalDetail } from './types';

export const PROFESSIONAL_DETAILS_FIXTURE: ProfessionalDetail[] = [{
  function: 'Rechter In Opleiding',
  id: '8a2ea390-61f1-4eae-bd20-4a162182e78c',
  organisation: 'Rechtbank Den Haag',
  start_date: "2022-11-01T00:00:00",
  end_date: null
},
{
  function: 'Rechter-Plaatsvervanger',
  id: 'ba21abea-9740-4f7b-8807-a9ca51b49816',
  organisation: 'Rechtbank Den Haag',
  start_date: "2020-01-01T00:00:00",
  end_date: null,
},
{
  function: 'Rechter',
  id: '5ea009b1-6825-4bce-a7d6-667e749766cd',
  organisation: 'Rechtbank Utrecht',
  start_date: "2020-01-01T00:00:00",
  end_date: "2023-01-01T00:00:00",
}];

export const PERSON_FIXTURE: Person = {
  id: '0eee8e7d-d402-47b1-8726-a5a2e430889f',
  toon_naam: 'mr. A.B.C. De Jong',
  professional_details: PROFESSIONAL_DETAILS_FIXTURE,
};
