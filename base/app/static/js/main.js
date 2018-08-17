$(document).ready(function () {
try{
    var sock = new WebSocket('ws://' + window.location.host + '/ws');
}
catch(err){
    var sock = new WebSocket('wss://' + window.location.host + '/ws');
}

function showMessage(message) {
    $('#message').text(message);
}

function sendMessage(message){
    sock.send(message);
}

function disableButtons(data){
    $('#activate').prop('checked', data.checked);
    $('.start').prop('disabled', data.disable);
    $('.stop').prop('disabled', data.disable);
    $('.restart').prop('disabled', data.disable);
}

function getClosestService(obj){
    return $(obj).closest('.service').data('name')
}

function changeServiceStatus(status, service){
    elem  = $('.srv_status[data-name="'+service+'"]');
    if (status) {
        $(elem).text('Статус сервиса: Запущен');
        console.log($(elem))
        $(elem).css('color', 'green');
    }
    else {
        $(elem).text('Статус сервиса: Не запущен');
        $(elem).css('color', 'red');
    }
}

// send message to start
$('.start').click(function() {
    sendMessage('{"type": "start", "service": "'+  getClosestService(this) +'"}');
});

// send message to stop
$('.stop').click(function() {
    sendMessage('{"type": "stop", "service": "'+  getClosestService(this) +'"}');
});

// send message to restart
$('.restart').click(function() {
    sendMessage('{"type": "restart", "service": "'+  getClosestService(this) +'"}');
});

$('#activate').change(function() {
    sendMessage('{"type": "activate", "checked": "'+ Number($("#activate").is(':checked')) +'"}');
});

sock.onopen = function(){
    showMessage('Connection to server started')
};

// income message
sock.onmessage = function(event) {
  data = jQuery.parseJSON(event.data)
  showMessage(data.text);
  if (data.success) {
    disableButtons(data)
    changeServiceStatus(data.status, data.service)
  }
};

sock.onclose = function(event){
    if(event.wasClean){
        showMessage('Clean connection end')
    }else{
        showMessage('Connection broken')
    }
};

sock.onerror = function(error){
    showMessage(error);
}
});