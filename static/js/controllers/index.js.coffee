Grades.controller 'IndexCtrl', ['$scope', '$window', '$timeout', 'API', '$cookies',
 ($scope, $window, $timeout, API, $cookies) ->

  $scope.data = angular.fromJson($cookies.data or '{}')
  $scope.user = {}
  $scope.auth = false

  checkAuth = (data) ->
    return unless data.kerberos and data.password
    API.post 'check_auth', data
    .then (response) ->
      $timeout ->
        $scope.auth = response.authenticated
        $scope.user = response.user
        $cookies.data = angular.toJson($scope.data)

  $scope.$watch 'data', checkAuth, true
]
