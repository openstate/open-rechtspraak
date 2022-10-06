import { Person, ProfessionalDetail } from './types';

export const PROFESSIONAL_DETAILS_FIXTURE: ProfessionalDetail[] = [{
  function: 'Rechter In Opleiding',
  id: '8a2ea390-61f1-4eae-bd20-4a162182e78c',
  organisation: 'Rechtbank Den Haag',
},
{
  function: 'Rechter-Plaatsvervanger',
  id: 'ba21abea-9740-4f7b-8807-a9ca51b49816',
  organisation: 'Rechtbank Den Haag',
}];

export const PERSON_FIXTURE: Person = {
  id: '0eee8e7d-d402-47b1-8726-a5a2e430889f',
  toon_naam: 'dhr. mr. A.B.C. De Jong',
  professional_details: PROFESSIONAL_DETAILS_FIXTURE,
};
