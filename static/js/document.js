$(document).ready(function() {

    namespace = '/';

    var socket = io(namespace);
    var text = "";

    socket.on('connect', function() {
        socket.emit('connection_established');
    });

    socket.on('disconnect', function() {
        socket.emit('connection_lost');
    });

    socket.on('result', function(result) {
        $("#result").html(result)
    });

    $("#input-text").keypress( function(event) {
        if (event.which == 13) {
            if (($(this).val() != "") && ($(this).val() != null)) {
                text = { "text": $(this).val(), "k": $("#k").val() };
                sendText();
            }
        }
    });

    sendText = function() {
        socket.emit('text_to_process', text);
        text = null;
    };
});