type Model = {
  id: string
};

export type ProfessionalDetail = Model & {
  function: string
  organisation: string
};

export type Person = Model & {
  toon_naam: string
  professional_details: ProfessionalDetail[]
};
