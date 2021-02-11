const uniqueOrganisations = (beroepsgegevens) => {
  let set = new Set();
  beroepsgegevens.forEach((bg) => {
    set.add(bg.organisation)
  })
  return set
}

const uniqueFunctions = (beroepsgegevens) => {
  let set = new Set();
  beroepsgegevens.forEach((bg) => {
    set.add(bg.function)
  })
  return set
}

const renderOrganisation = (person) => {
  let html = '';
  for (let bg of uniqueOrganisations(person.beroepsgegevens).values()) {
    html += '<span class="badge rounded-pill bg-primary ms-2">' + bg + '</span>'
  }
  for (let bg of uniqueFunctions(person.beroepsgegevens).values()) {
    html += '<span class="badge rounded-pill bg-secondary ms-2">' + bg + '</span>'
  }
  return html
}

export const personTemplate = (person) => {
  const name = person.toon_naam
  const func = person.beroepsgegevens[0]?.function || ''
  const organisation = person.beroepsgegevens[0]?.organisation || ''
  return `
        <a class="search-result-person" href="person/${person.id}">
          <div class="card mb-3">
            <div class="card-body">
              <h3 class="search-result-person__name">${name}</h3>
              <h4 class="text-secondary">${func}</h4>
            </div>
            <div class="card-footer">
            ${renderOrganisation(person)}</span>
            </div>
          </div>
        </a>
        `}
