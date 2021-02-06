export const personTemplate = (person) => {
  return `
        <a class="search-result-person" href="person/${person.id}">
          <div class="card mb-3">
            <div class="card-body">
              <h3>${person.toon_naam}</h3>
            </div>
          </div>
        </a>
        `}
