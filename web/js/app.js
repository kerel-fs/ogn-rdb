var ognrdbApp = angular.module('ognrdbApp',[
  'ngRoute',
  'ognrdbControllers'
]);

ognrdbApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/receivers', {
        templateUrl: 'partials/receiver-list.html',
        controller: 'ReceiverListCtrl'
      }).
      when('/receivers/:callsign', {
        templateUrl: 'partials/receiver-detail.html',
        controller: 'ReceiverDetailCtrl'
      }).
      otherwise({
        redirectTo: '/receivers'
      });
  }]);
