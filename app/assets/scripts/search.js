import {personTemplate} from './templates';

const doSearch = () => {
  $.get({
    url: url(),
  }).done((data) => {
    bindCount(data.count);
    bindResults(data.data)
  })
}

const bindCount = (count) => {
  $("#search-results-count").text(count)
}

const clearResults = () => {
  $('#results').empty();
}

const bindResults = (people) => {
  clearResults();
  people.forEach((person) => {
    let personHtml = personTemplate(person);
    $("#results").append(personHtml);
  })
}

const getSearchValue = () => {
  return $("#q").val();
}

const url = () => {
  const params = new URLSearchParams({
    q: getSearchValue()
  })
  const queryString = params.toString();
  return `/api/v1/search?${queryString}`;
}

$(document).ready(function () {
  doSearch();

  $("#q").on('input', () => {
    doSearch()
  })
});
