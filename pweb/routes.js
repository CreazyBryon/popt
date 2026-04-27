const { URL } = require('url');
const controller = require('./controller');
const popController = require('./pop-controller');

const routeHandlers = {
	'GET /': controller.getRoot,
	'GET /health': controller.getHealth,
	'GET /api/hello': controller.getHello,
	'POST /api/echo': controller.postEcho,

	'GET /api/pop/logs': popController.getLogs,
    'POST /api/pop/logs': popController.addLog,
    'GET /page/pop/logs': popController.getLogPage,
};

const buildContext = (request, response) => {
	const url = new URL(request.url, `http://${request.headers.host || 'localhost'}`);
	const routeKey = `${request.method} ${url.pathname}`;

	return {
		request,
		response,
		url,
		searchParams: url.searchParams,
		routeKey,
	};
	};

const handleRequest = async (request, response) => {
	const context = buildContext(request, response);
	const handler = routeHandlers[context.routeKey] || controller.notFound;

	await handler(context);
};

module.exports = {
	handleRequest,
};