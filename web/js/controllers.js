var ognrdbControllers = angular.module('ognrdbControllers', []);

ognrdbControllers.controller('ReceiverListCtrl', function($scope, $http) {
  $http.get("https://ogn.peanutpod.de/receivers.json")
        .success(function (data) {
            $scope.receiversdb = data;
        });

  $scope.toggle = function(receiver) {
    receiver.showDetails = !receiver.showDetails;
  }
});
