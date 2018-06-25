var ognrdbControllers = angular.module('ognrdbControllers', []);

ognrdbControllers.controller('ReceiverListCtrl', function($scope, $http, $q) {
    $scope.receivers = {};
    $scope.loading = true;

    loading_done = function () {
        $scope.loading = false;
    };

    update_aprsc_status = function (response) {
        angular.forEach(response.data.clients, function(client) {
            if ($scope.receivers[client.username]) {
                $scope.receivers[client.username].aprsc_status = client;
            } else if (client.app_name == "RTLSDR-OGN" || client.app_name == "ogn-decode" ) {
                // app_name='ogn-decode' is a bug in a beta version of v0.2.5
                $scope.receivers[client.username] = {'callsign': client.username};
            }
        });
    }

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
        });

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
            angular.forEach(response.data.receivers, function(value, key) {
                if (!$scope.receivers[key]) {
                    $scope.receivers[key] = {'callsign': key};
                }
                $scope.receivers[key].privacy = value;
            });
        });

    glidern1_p = $http.get("https://ogn.peanutpod.de/glidern1/status.json")
        .then(update_aprsc_status).finally();
    glidern2_p = $http.get("https://ogn.peanutpod.de/glidern2/status.json")
        .then(update_aprsc_status).finally();
    glidern3_p = $http.get("https://ogn.peanutpod.de/glidern3/status.json")
        .then(update_aprsc_status).finally();
    glidern4_p = $http.get("https://ogn.peanutpod.de/glidern4/status.json")
        .then(update_aprsc_status).finally();

    intern_p = $q.all([receivers_p, privacy_p, glidern1_p, glidern2_p, glidern3_p, glidern4_p]).finally(update_receivers).finally(loading_done);

    all_p = $q.all([intern_p, ognrange_p]).then(update_receivers);

    $scope.toggle_details = function(receiver) {
        receiver.showDetails = !receiver.showDetails;
    }

    $scope.predicate = ['callsign'];
    $scope.reverse = false;
    $scope.order = function(predicate) {
      $scope.reverse = ($scope.predicate[0] === predicate[0]) ? !$scope.reverse : false;
      $scope.predicate = predicate;
    };
});

ognrdbControllers.controller('ReceiverDetailCtrl', ['$scope', '$routeParams', '$http', '$controller',
  function($scope, $routeParams, $http, $controller) {
    $controller('ReceiverListCtrl', {$scope: $scope});
    update_receiver = function () {
        $scope.receiver = $scope.receivers[$routeParams.callsign];
    };
    intern_p.then(update_receiver);
    all_p.then(update_receiver);
  }]);
