"""Simple REST client helpers.

This module provides a small reusable HTTP client built on the Python
standard library so it can be imported without extra dependencies.
"""

from __future__ import annotations

import json
import socket
from dataclasses import dataclass
import threading
from typing import Any, Dict, List, Mapping, Optional, Union
from urllib import error, parse, request


Headers = Optional[Mapping[str, str]]
Params = Optional[Mapping[str, Any]]
Payload = Optional[Union[Mapping[str, Any], List[Any]]]


class HttpError(Exception):
	"""Raised when an HTTP request fails."""

	def __init__(self, status_code: int, message: str, body: str = ""):
		super().__init__(message)
		self.status_code = status_code
		self.body = body


@dataclass
class HttpResponse:
	status_code: int
	headers: Dict[str, str]
	text: str

	def json(self) -> Any:
		return json.loads(self.text) if self.text else None


class RestClient:
	def __init__(
		self,
		base_url: str,
		*,
		timeout: float = 10.0,
		headers: Headers = None,
	):
		self.base_url = base_url.rstrip("/")
		self.timeout = timeout
		self.default_headers = dict(headers or {})

	def build_url(self, path: str, params: Params = None) -> str:
		url = f"{self.base_url}/{path.lstrip('/')}"
		if not params:
			return url

		query = parse.urlencode(params, doseq=True)
		separator = "&" if "?" in url else "?"
		return f"{url}{separator}{query}"

	def request(
		self,
		method: str,
		path: str,
		*,
		params: Params = None,
		headers: Headers = None,
		json_body: Payload = None,
		data: Optional[bytes] = None,
	) -> HttpResponse:
		merged_headers = {**self.default_headers, **dict(headers or {})}
		body = data

		if json_body is not None:
			body = json.dumps(json_body).encode("utf-8")
			merged_headers.setdefault("Content-Type", "application/json")
 
		req = request.Request(
			self.build_url(path, params=params),
			data=body,
			headers=merged_headers,
			method=method.upper(),
		)

		try:
			with request.urlopen(req, timeout=self.timeout) as response:
				payload = response.read().decode("utf-8")
				return HttpResponse(
					status_code=response.getcode(),
					headers=dict(response.headers.items()),
					text=payload,
				)
		except error.HTTPError as exc:
			body_text = exc.read().decode("utf-8", errors="replace")
			print(f"HTTP error {exc.code}: {exc.reason}\nResponse body: {body_text}")
			raise HttpError(exc.code, f"HTTP {exc.code}: {exc.reason}", body_text) from exc
		except error.URLError as exc:
			reason = exc.reason
			if isinstance(reason, socket.timeout):
				raise TimeoutError("Request timed out") from exc
			raise ConnectionError(f"Request failed: {reason}") from exc

	def get(self, path: str, *, params: Params = None, headers: Headers = None) -> HttpResponse:
		return self.request("GET", path, params=params, headers=headers)

	def post(
		self,
		path: str,
		*,
		params: Params = None,
		headers: Headers = None,
		json_body: Payload = None,
		data: Optional[bytes] = None,
	) -> HttpResponse:
		return self.request("POST", path, params=params, headers=headers, json_body=json_body, data=data)

	def put(
		self,
		path: str,
		*,
		params: Params = None,
		headers: Headers = None,
		json_body: Payload = None,
		data: Optional[bytes] = None,
	) -> HttpResponse:
		return self.request("PUT", path, params=params, headers=headers, json_body=json_body, data=data)

	def patch(
		self,
		path: str,
		*,
		params: Params = None,
		headers: Headers = None,
		json_body: Payload = None,
		data: Optional[bytes] = None,
	) -> HttpResponse:
		return self.request("PATCH", path, params=params, headers=headers, json_body=json_body, data=data)

	def delete(self, path: str, *, params: Params = None, headers: Headers = None) -> HttpResponse:
		return self.request("DELETE", path, params=params, headers=headers)


def get(url: str, *, timeout: float = 10.0, headers: Headers = None, params: Params = None) -> HttpResponse:
	return RestClient(_base_url(url), timeout=timeout, headers=headers).get(_path(url), params=params)


def post(
	url: str,
	*,
	timeout: float = 10.0,
	headers: Headers = None,
	params: Params = None,
	json_body: Payload = None,
	data: Optional[bytes] = None,
) -> HttpResponse:
	print(f"Making POST request to {url} with params={params}, json_body={json_body}, data={data}")
	return RestClient(_base_url(url), timeout=timeout, headers=headers).post(
		_path(url),
		params=params,
		json_body=json_body,
		data=data,
	)

def apost(
    url: str,
    *,
    timeout: float = 10.0,
    headers: Headers = None,
    params: Params = None,
    json_body: Payload = None,
    data: Optional[bytes] = None,
) -> threading.Thread:
    thread = threading.Thread(
        target=_post_background,
        args=(url,),
        kwargs={
            "timeout": timeout,
            "headers": headers,
            "params": params,
            "json_body": json_body,
            "data": data,
        },
        daemon=True,
    )
    thread.start()
    return thread


def put(
	url: str,
	*,
	timeout: float = 10.0,
	headers: Headers = None,
	params: Params = None,
	json_body: Payload = None,
	data: Optional[bytes] = None,
) -> HttpResponse:
	return RestClient(_base_url(url), timeout=timeout, headers=headers).put(
		_path(url),
		params=params,
		json_body=json_body,
		data=data,
	)


def patch(
	url: str,
	*,
	timeout: float = 10.0,
	headers: Headers = None,
	params: Params = None,
	json_body: Payload = None,
	data: Optional[bytes] = None,
) -> HttpResponse:
	return RestClient(_base_url(url), timeout=timeout, headers=headers).patch(
		_path(url),
		params=params,
		json_body=json_body,
		data=data,
	)


def delete(url: str, *, timeout: float = 10.0, headers: Headers = None, params: Params = None) -> HttpResponse:
	return RestClient(_base_url(url), timeout=timeout, headers=headers).delete(_path(url), params=params)


def _post_background(
    url: str,
    *,
    timeout: float = 10.0,
    headers: Headers = None,
    params: Params = None,
    json_body: Payload = None,
    data: Optional[bytes] = None,
) -> None:
    try:
        post(
            url,
            timeout=timeout,
            headers=headers,
            params=params,
            json_body=json_body,
            data=data,
        )
    except Exception as exc:
        print(f"Background POST failed for {url}: {exc}")

def _base_url(url: str) -> str:
	parsed = parse.urlsplit(url)
	if not parsed.scheme or not parsed.netloc:
		raise ValueError("URL must include scheme and host")
	return f"{parsed.scheme}://{parsed.netloc}"


def _path(url: str) -> str:
	parsed = parse.urlsplit(url)
	path = parsed.path or "/"
	if parsed.query:
		return f"{path}?{parsed.query}"
	return path


__all__ = [
	"HttpError",
	"HttpResponse",
	"RestClient",
	"delete",
	"get",
	"patch",
	"post",
	"put",
]
