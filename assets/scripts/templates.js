const renderOrganisation = (person) => {
  let html = '';
  person.beroepsgegevens.forEach((bg) => {
      console.log(bg);
    html += '<span class="badge rounded-pill bg-primary ms-2">' + bg.organisation + '</span>'
  })
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
