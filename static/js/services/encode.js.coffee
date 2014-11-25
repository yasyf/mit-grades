Grades.factory "Encode", ->

  Encode =
    encode: (originalData) ->
      data = angular.copy(originalData)
      data.password = btoa data.password if data.password
      data
    decode: (originalData) ->
      data = angular.copy(originalData)
      data.password = atob data.password if data.password
      data

  Encode
