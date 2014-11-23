Grades.controller 'IndexCtrl', ['$scope', '$window', '$timeout', 'API', '$cookies',
 ($scope, $window, $timeout, API, $cookies) ->

  $scope.good_bound = 0.86

  $scope.data = angular.fromJson($cookies.data or '{}')
  $scope.user = {}
  $scope.grades = {}
  $scope.status = 'Login To Begin'
  $scope.auth = false
  $scope.selected = null

  checkAuth = (data) ->
    return unless data.kerberos and data.password
    $scope.status = 'Authenticating'
    API.post 'check_auth', data
    .then (response) ->
      $timeout ->
        $scope.auth = response.authenticated
        $scope.user = response.user
        $cookies.data = angular.toJson($scope.data)
        $scope.status = 'Login To Begin' unless response.authenticated

  getGrades = (auth) ->
    return unless auth
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
]
