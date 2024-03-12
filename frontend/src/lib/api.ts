import { error } from '@sveltejs/kit';

const API_URL: string = 'http://nginx/api';

async function send({
	method,
	path,
	data,
	token
}: {
	method: string;
	path: string;
	data?: any;
	token?: string;
}): Promise<any> {
	const opts: { method: string; headers: Record<string, string>; body?: string } = {
		method,
		headers: {}
	};

	if (data) {
		opts.body = JSON.stringify(data);
	}

	opts.headers['credentials'] = `include`;

	const res = await fetch(`${API_URL}${path}`, opts);
	if (res.ok || res.status === 422) {
		const body = await res.json();
		return body;
	}

	throw error(res.status);
}

export function get(path: string, token?: string): Promise<any> {
	return send({ method: `GET`, path, token });
}

export function post(path: string, data: any, token?: string): Promise<any> {
	return send({ method: `POST`, path, data, token });
}

export function put(path: string, data: any, token?: string): Promise<any> {
	return send({ method: `PUT`, path, data, token });
}

export function del(path: string, data: any, token?: string): Promise<any> {
	return send({ method: `DELETE`, path, data, token });
}
