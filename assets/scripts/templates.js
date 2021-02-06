export const personTemplate = (person) => {
  return `
        <a class="search-result-person" href="person/${person.id}">
          <div class="card mb-3">
            <div class="card-body">
              <h3 class="search-result-person__name">${person.toon_naam}</h3>
            </div>
          </div>
        </a>
        `}
