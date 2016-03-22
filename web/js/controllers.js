var ognrdbControllers = angular.module('ognrdbControllers', []);

ognrdbControllers.controller('ReceiverListCtrl', function($scope, $http) {
  $http.get("https://ogn.peanutpod.de/receivers.json")
        .success(function (data) {
            $scope.receiversdb = data;
        });
  $http.get("https://ognrange.onglide.com/api/1/stations")
        .success(function (data) {
            $scope.receiverstats = {};
            for (i = 0; i < data.stations.length; i++) {
                $scope.receiverstats[data.stations[i].s] = data.stations[i];
            }
        });

  $scope.toggle = function(receiver) {
    receiver.showDetails = !receiver.showDetails;
  }
});

ognrdbControllers.controller('ReceiverDetailCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {
    $http.get("https://ogn.peanutpod.de/receivers.json")
        .success(function (data) {
            $scope.receiver = data.receivers.filter(function (el) { return el.callsign == $routeParams.callsign;})[0];
            $scope.receiver.image = $scope.receiver.photos[0] ? $scope.receiver.photos[0]:'';
        });

    $http.get("https://ognrange.onglide.com/api/1/stations")
          .success(function (data) {
              receiverstats = {};
              for (i = 0; i < data.stations.length; i++) {
                  receiverstats[data.stations[i].s] = data.stations[i];
              }
              $scope.stats = receiverstats[$routeParams.callsign];
          });
  }]);
