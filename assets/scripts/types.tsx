interface Model {
  id: string;
}

export interface ProfessionalDetail extends Model {
  function: string;
  organisation: string;
}

export interface Person extends Model {
  toon_naam: string;
  professional_details: ProfessionalDetail[];
}
