$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number " + msg.number);
        $('#count').html(msg.number);
    });
});