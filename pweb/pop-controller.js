const fs = require('fs/promises');
const path = require('path');
const { readJsonBody, sendHtml, sendJson } = require('./utils/http-helper');

const popLogs={

	logs:[{
		timestamp: new Date().toISOString(), 
		message: 'Pop controller initialized.'
	}]
	 
}

const escapeHtml = (value) => String(value)
	.replace(/&/g, '&amp;')
	.replace(/</g, '&lt;')
	.replace(/>/g, '&gt;')
	.replace(/"/g, '&quot;')
	.replace(/'/g, '&#39;');

const getLogs = async ({ response, searchParams }) => {
	const limit = Math.min(Math.max(parseInt(searchParams.get('limit')) || 100, 1), 1000);
	const logsToReturn = popLogs.logs.slice(-limit);


	sendJson(response, 200, {
		controller: 'popController',
		data: logsToReturn,
	});
};

const addLog = async ({ request, response }) => {
	try {
		const body = await readJsonBody(request);
		console.log('Received request body:', body);
		const { message } = body;

		if (typeof message !== 'string') {
			sendJson(response, 400, {
				error: 'Message must be a string.',
			});
			return;
		}

		popLogs.logs.push({
			timestamp: new Date().toISOString(),
			message,
		});

		sendJson(response, 200, {
			message: 'Log added successfully.'
		});
	} catch {
		sendJson(response, 400, {
			error: 'Request body must be valid JSON.',
		});
	}
};

const getLogPage = async ({ response }) => {
    const htmlPath = path.join(__dirname, 'logs.html');
    const html = await fs.readFile(htmlPath, 'utf8');

	sendHtml(response, 200, html);
};

  

module.exports = {
	getLogPage,
	getLogs,
	addLog,
};