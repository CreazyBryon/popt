const sendJson = (response, statusCode, body) => {
	response.writeHead(statusCode, { 'Content-Type': 'application/json; charset=utf-8' });
	response.end(JSON.stringify(body));
};

const sendHtml = (response, statusCode, html) => {
	response.writeHead(statusCode, { 'Content-Type': 'text/html; charset=utf-8' });
	response.end(html);
};

const readJsonBody = async (request) => {
	const chunks = [];

	for await (const chunk of request) {
		chunks.push(chunk);
	}

	if (chunks.length === 0) {
		return null;
	}

	const rawBody = Buffer.concat(chunks).toString('utf8').trim();

	if (!rawBody) {
		return null;
	}

	return JSON.parse(rawBody);
};

module.exports = {
	readJsonBody,
	sendHtml,
	sendJson,
};