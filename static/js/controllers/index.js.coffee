Grades.controller 'IndexCtrl', ['$scope', '$window', '$timeout', 'API', '$cookies',
 ($scope, $window, $timeout, API, $cookies) ->

  $scope.good_bound = 0.86

  $scope.data = angular.fromJson($cookies.data or '{}')
  $scope.user = {}
  $scope.grades = {}
  $scope.status = 'Login To Begin'
  $scope.auth = false
  $scope.selected = null

  encodePassword = (originalData) ->
    data = angular.copy(originalData)
    data.password = btoa data.password
    data

  checkAuth = _.debounce (data) ->
    return unless data.kerberos and data.password
    $timeout ->
      $scope.status = 'Authenticating'
    API.post 'check_auth', encodePassword(data)
    .then (response) ->
      $timeout ->
        $scope.auth = response.authenticated
        $scope.user = response.user
        $cookies.data = angular.toJson($scope.data)
        $scope.status = 'Login To Begin' unless response.authenticated
  , 250

  getGrades = (auth) ->
    unless auth
      $scope.grades = {}
      return
    $scope.status = 'Loading'
    API.post 'grades', encodePassword($scope.data)
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
]
