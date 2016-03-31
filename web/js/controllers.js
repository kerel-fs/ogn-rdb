var ognrdbControllers = angular.module('ognrdbControllers', []);

ognrdbControllers.controller('ReceiverListCtrl', function($scope, $http, $q) {
    $scope.receivers = {};
    update_receivers = function() {
        $scope.receivers_list = [];
        angular.forEach($scope.receivers, function(value, key) {
            $scope.receivers_list.push(value);
        });
    };

    receivers_p = $http.get("https://ogn.peanutpod.de/receivers.json")
        .then(function (response) {
            $scope.receiversdb_timestamp = response.data.timestamp;
            angular.forEach(response.data.receivers, function(receiver) {
                if (!$scope.receivers[receiver.callsign]) {
                    $scope.receivers[receiver.callsign] = {'callsign':receiver.callsign};
                }
                $scope.receivers[receiver.callsign].rdb = receiver;
            });
        }).then(update_receivers);

    ognrange_p = $http.get("https://ognrange.onglide.com/api/1/stations")
        .then(function (response) {
            angular.forEach(response.data.stations, function(station) {
                if (!$scope.receivers[station.s]) {
                    $scope.receivers[station.s] = {'callsign': station.s};
                }
                $scope.receivers[station.s].stats = station;
            });
        });

    $q.all([receivers_p, ognrange_p, privacy_p]).then(update_receivers);

    $scope.in_rdb = function(receiver, options) {
        return ((receiver && receiver.rdb) || $scope.show_unregistered);
    };

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
