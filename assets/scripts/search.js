import {personTemplate} from './templates';

const doSearch = () => {
  $.get({
    url: url(),
    success: (data) => {
      bindCount(data.count);
      bindResults(data.data);
    },
    complete: setWindowUrl()
  })
}

const setWindowUrl = () => {
  window.history.pushState({}, '', '?' + queryString());
}

const populateSearchField = () => {
  const urlParams = new URLSearchParams(window.location.search);
  $("#q").val(urlParams.get('q'));
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

const queryString = () => {
  const params = new URLSearchParams({
    q: getSearchValue()
  })
  return params.toString();
}

const url = () => {
  return `/api/v1/search?${queryString()}`;
}

$(document).ready(function () {
  if ($('#results').length > 0) {
    populateSearchField();
    doSearch();
  }

  $("#q").on('input', () => {
    doSearch()
  })
});
