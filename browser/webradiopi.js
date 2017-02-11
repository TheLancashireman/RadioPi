var socket;

window.onload = function() {

	// Create a new WebSocket.
	var hostname = '192.168.8.21';
	if (window.location.hostname != '') {
		hostname = window.location.hostname;
	}
//	var hostname = 'radiopi';
	socket = new WebSocket('ws://' + hostname + ':6502');

	// Handle any errors that occur.
	socket.onerror = function(error) {
		console.log('WebSocket Error: ' + error);
	};

	// Show a connected message when the WebSocket is opened.
	socket.onopen = function(event) {
		console.log('Connected to: ' + event.currentTarget.URL);
	};

	// Handle messages sent by the server.
	socket.onmessage = function(event) {
		var message = event.data;
		console.log('Message received: ' + message);
	};

	// Show a disconnected message when the WebSocket is closed.
	socket.onclose = function(event) {
		alert('Disconnected from WebSocket.');
	};
};

// close the socket before leaving.
// See https://stackoverflow.com/questions/4812686/closing-websocket-correctly-html5-javascript#481854
window.onbeforeunload = function() {
    socket.onclose = function () {}; // disable onclose handler first
    socket.close()
};

// Performs add and addall
rp_add = function(f) {
	var message = 'add ' + f;
	socket.send(message)
}

// Performs parameterless command
rp_cmd = function(c) {
	socket.send(c)
}

// Goes back to previous page
rp_back = function() {
	window.history.back()
}

// Performs parameterless command and goes back to previous page
rp_cmdback = function(c) {
	socket.send(c);
	window.history.back()
}

// Performs mount
rp_mount = function(f) {
	var message = 'mount ' + f;
	socket.send(message);
	window.history.back()
}

// Performs radio station selection
rp_station = function(f) {
	var message = 'station ' + f;
	socket.send(message);
	window.history.back()
}
