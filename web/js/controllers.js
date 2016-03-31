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

    privacy_p = $http.get("https://ogn.peanutpod.de/receivers-privacy.json")
        .then(function (response) {
            angular.forEach(response.data, function(value, key) {
                if (!$scope.receivers[key]) {
                    $scope.receivers[key] = {'callsign': key};
                }
                $scope.receivers[key].privacy = value;
            });
        });

    $q.all([receivers_p, ognrange_p, privacy_p]).then(update_receivers);

    $scope.filter_in_rdb = function(receiver, options) {
        return ((receiver && receiver.rdb) || $scope.show_rdb_only);
    };

    $scope.toggle_details = function(receiver) {
        receiver.showDetails = !receiver.showDetails;
    }

    $scope.ddb_filter_state = "show-all";
    $scope.filter_respects_ddb = function(receiver) {
        if ($scope.ddb_filter_state == "show-all") {
            return true;
        } else if ($scope.ddb_filter_state == "show-legal") {
            return (receiver.privacy && receiver.privacy.respects_ddb);
        } else {
            return (receiver.privacy && !receiver.privacy.respects_ddb);
        }
    };
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
