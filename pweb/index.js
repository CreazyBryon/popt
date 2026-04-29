
const http = require('http');
const routes = require('./routes');

const port = Number(process.env.PORT) || 3000;

const server = http.createServer(async (request, response) => {
	try {
		await routes.handleRequest(request, response);
	} catch (error) {
		response.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
		response.end(JSON.stringify({
			error: 'Internal server error.',
			details: process.env.NODE_ENV === 'development' ? error.message : undefined,
		}));
	}
});
const start = async () => {
	await routes.initialize();

	server.listen(port, () => {
		console.log(`API service listening on http://localhost:${port}`);
	});
};

start().catch((error) => {
	console.error('Failed to start server:', error);
	process.exit(1);
});
