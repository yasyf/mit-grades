Grades.factory "LocalStorage", ['Encode', (Encode) ->

  LocalStorage =
    set: (key, value) ->
      localStorage[key] = btoa angular.toJson(Encode.encode value)
    get: (key, def='{}') ->
      Encode.decode angular.fromJson(if localStorage[key] then atob(localStorage[key]) else def)

  LocalStorage
]
