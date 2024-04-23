import { browser } from '$app/environment';

const api_route = 'http://localhost/api';
export default {
	async updateInterests(interests: number[]) {
		try {
			const response = await fetch(`${api_route}/user/interests/edit`, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					tags: interests
				})
			});
			if (response.status === 401) {
				const newTokens = await this.refreshToken();
				if (newTokens) {
					if (browser) {
						// document.cookie = `access_zhopen=Bearer ${newTokens.access_token}; expires=Thu, 01 Jan 2025 00:00:00 GMT; path=/`;
					}
				} else {
					throw new Error('Failed to refresh access token');
				}
			} else {
				throw new Error(`API request failed with status: ${response.status}`);
			}
		} catch (error) {
			console.error('Error updating interests:', error);
		}
	},
	async updateTripPurposes(tripPurposes: number[]) {
		await fetch(`${api_route}/user/trip_purposes/edit`, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				tags: tripPurposes
			})
		});
	},
	async updateDepartures(departures: number[]) {
		await fetch(`${api_route}/user/departures/edit`, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				locations: departures
			})
		});
	},
	async updateArrivals(arrivals: number[]) {
		await fetch(`${api_route}/user/arrivals/edit`, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				locations: arrivals
			})
		});
	},
	async refreshToken() {
		const response = await fetch(`${api_route}/auth/refresh`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (response.ok) {
			const data = await response.json();
			return data; // Return the new access and refresh tokens
		} else {
			throw new Error('Failed to refresh access token');
		}
	}
};
