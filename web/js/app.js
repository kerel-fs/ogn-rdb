var ognrdbApp = angular.module('ognrdbApp',[
  'ngRoute',
  'ognrdbControllers'
]);

ognrdbApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/receivers', {
        title: 'OGN Receivers list',
        templateUrl: 'partials/receiver-list.html',
        controller: 'ReceiverListCtrl'
      }).
      when('/receivers/:callsign', {
        title: ' - OGN Receivers list',
        templateUrl: 'partials/receiver-detail.html',
        controller: 'ReceiverDetailCtrl'
      }).
      otherwise({
        redirectTo: '/receivers'
      });
  }]);

ognrdbApp.run(['$rootScope', function($rootScope) {
    $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
        $rootScope.title = current.$$route.title;
        if(current.params.callsign)
            $rootScope.title = current.params.callsign + $rootScope.title;
    });
}]);
