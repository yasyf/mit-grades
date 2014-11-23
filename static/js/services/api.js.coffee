Grades.factory "API", ->
  API =
    get: (action, qs = {}) ->
      $.ajax
        type: 'GET'
        url: "/api/#{action}?#{$.param(qs)}"
    delete: (action, data, qs = {}) ->
      $.ajax
        type: 'DELETE'
        url: "/api/#{action}?#{$.param(qs)}"
        data: data or {}
    post: (action, data, qs = {}) ->
      $.ajax
        type: 'POST'
        url: "/api/#{action}?#{$.param(qs)}"
        data: JSON.stringify(data)
        contentType: 'application/json'
        dataType: 'json'

  API
