Grades.factory "API", ['Encode', (Encode) ->
  API =
    get: (action, qs = {}) ->
      $.ajax
        type: 'GET'
        url: "/api/#{action}?#{$.param(qs)}"
      .then (result) ->
        Encode.decode result
    delete: (action, data, qs = {}) ->
      $.ajax
        type: 'DELETE'
        url: "/api/#{action}?#{$.param(qs)}"
        data: Encode.encode data or {}
      .then (result) ->
        Encode.decode result
    post: (action, data, qs = {}) ->
      $.ajax
        type: 'POST'
        url: "/api/#{action}?#{$.param(qs)}"
        data: JSON.stringify(Encode.encode data)
        contentType: 'application/json'
        dataType: 'json'
      .then (result) ->
        Encode.decode result

  API
]
