Grades.controller 'IndexCtrl', ['$scope', '$window', '$timeout', 'API', '$cookies',
 ($scope, $window, $timeout, API, $cookies) ->

  $scope.good_bound = 0.86

  $scope.data = angular.fromJson($cookies.data or '{}')
  $scope.user = {}
  $scope.grades = {}
  $scope.auth = false

  checkAuth = (data) ->
    return unless data.kerberos and data.password
    API.post 'check_auth', data
    .then (response) ->
      $timeout ->
        $scope.auth = response.authenticated
        $scope.user = response.user
        $cookies.data = angular.toJson($scope.data)

  getGrades = (auth) ->
    return unless auth
    API.post 'grades', $scope.data
    .then (response) ->
      $timeout ->
        $scope.grades = response.grades

  $scope.$watch 'data', checkAuth, true
  $scope.$watch 'auth', getGrades

  $scope.remove_blank_categories = (category) ->
    category.avg > 0
]
