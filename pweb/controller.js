const { readJsonBody, sendJson } = require('./utils/http-helper');

const getRoot = async ({ response }) => {
	sendJson(response, 200, {
		name: 'pop-api',
		status: 'running',
		endpoints: ['/health', '/api/hello', '/api/echo', '/api/pop', '/pop/page'],
	});
};

const getHealth = async ({ response }) => {
	sendJson(response, 200, {
		status: 'ok',
		uptime: process.uptime(),
		timestamp: new Date().toISOString(),
	});
};


const getHello = async ({ response, searchParams }) => {
	const name = searchParams.get('name') || 'world';

	sendJson(response, 200, {
		message: `Hello, ${name}!`,
	});
};

const postEcho = async ({ request, response }) => {
	try {
		const body = await readJsonBody(request);
		sendJson(response, 200, { body });
	} catch {
		sendJson(response, 400, { error: 'Request body must be valid JSON.' });
	}
};

const notFound = async ({ response }) => {
	sendJson(response, 404, { error: 'Route not found.' });
};

module.exports = {
	getRoot,
	getHealth,
	getHello,
	postEcho,
	notFound,
};