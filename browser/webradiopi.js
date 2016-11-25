var socket;

window.onload = function() {

	// Create a new WebSocket.
	var hostname = 'localhost';
	if (window.location.hostname != '') {
		hostname = window.location.hostname;
	}
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

// Performs add and addall
rp_add = function(f) {
	var message = 'add ' + f;
	socket.send(message)
}
