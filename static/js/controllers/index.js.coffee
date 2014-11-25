Grades.controller 'IndexCtrl', ['$scope', '$window', '$timeout', 'API', 'LocalStorage'
 ($scope, $window, $timeout, API, LocalStorage) ->

  $scope.good_bound = 0.69

  $scope.data = LocalStorage.get 'data'
  $scope.user = {}
  $scope.grades = {}
  $scope.status = 'Login To Begin'
  $scope.auth = false
  $scope.selected = null
  $scope.detail = 0

  checkAuth = _.debounce (data) ->
    return unless data.kerberos and data.password
    $timeout ->
      $scope.status = 'Authenticating'
    API.post 'check_auth', data
    .then (response) ->
      $timeout ->
        $scope.auth = response.authenticated
        $scope.user = response.user
        LocalStorage.set 'data', $scope.data
        $scope.status = 'Login To Begin' unless response.authenticated
  , 250

  getGrades = (auth) ->
    unless auth
      $scope.grades = {}
      return
    $scope.status = 'Loading'
    API.post 'grades', $scope.data
    .then (response) ->
      $timeout ->
        $scope.grades = response.grades
        $scope.status = null

  $scope.$watch 'data', checkAuth, true
  $scope.$watch 'auth', getGrades

  $scope.remove_blank_categories = (category) ->
    category.avg > 0

  $scope.select_category = (category) ->
    if $scope.selected is category
      $scope.selected = null
    else
      $scope.selected = category

  $scope.toggle_detail = ->
    $scope.detail = if $scope.detail is 0 then 1 else 0
]
