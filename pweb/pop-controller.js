const fs = require('fs/promises');
const path = require('path');
const { readJsonBody, sendHtml, sendJson } = require('./utils/http-helper');

const logFilePath = path.join(__dirname, 'pop-logs.json');

const popLogs={

	logs:[]
	 
}

let loaded = false;
let loadPromise = null;

const escapeHtml = (value) => String(value)
	.replace(/&/g, '&amp;')
	.replace(/</g, '&lt;')
	.replace(/>/g, '&gt;')
	.replace(/"/g, '&quot;')
	.replace(/'/g, '&#39;');

const saveLogs = async () => {
	await fs.writeFile(
		logFilePath,
		JSON.stringify({ logs: popLogs.logs }, null, 2),
		'utf8'
	);
};

const ensureLoaded = async () => {
	if (loaded) {
		return;
	}

	if (!loadPromise) {
		loadPromise = (async () => {
			try {
				const raw = await fs.readFile(logFilePath, 'utf8');
				const parsed = JSON.parse(raw);

				popLogs.logs = Array.isArray(parsed?.logs) ? parsed.logs : [];
			} catch (error) {
				if (error.code !== 'ENOENT') {
					throw error;
				}

				popLogs.logs = [{
					timestamp: new Date().toISOString(),
					message: 'Pop controller initialized.'
				}];

				await saveLogs();
			}

			loaded = true;
		})();
	}

	await loadPromise;
};

const getLogs = async ({ response, searchParams }) => {
	await ensureLoaded();

	const limit = Math.min(Math.max(parseInt(searchParams.get('limit')) || 100, 1), 1000);
	const logsToReturn = popLogs.logs.slice(-limit);


	sendJson(response, 200, {
		controller: 'popController',
		data: logsToReturn,
	});
};

const addLog = async ({ request, response }) => {
	try {
		await ensureLoaded();

		const body = await readJsonBody(request);
		console.log('Received request body:', body);
		const { message,time } = body;
 
		popLogs.logs.push({
			timestamp: time || new Date().toISOString(),
			message,
		});

		await saveLogs();

		sendJson(response, 200, {
			message: 'Log added successfully.'
		});
	} catch {
		sendJson(response, 400, {
			error: 'Request body must be valid JSON.',
		});
	}
};

const clearLogs = async ({ response }) => {
	await ensureLoaded();

	popLogs.logs = [];
	await saveLogs();

	sendJson(response, 200, {
		message: 'Logs cleared successfully.'
	});
};

const getLogPage = async ({ response }) => {
    const htmlPath = path.join(__dirname, 'logs.html');
    const html = await fs.readFile(htmlPath, 'utf8');

	sendHtml(response, 200, html);
};

  

module.exports = {
	ensureLoaded,
	getLogPage,
	getLogs,
	addLog,
	clearLogs,
};