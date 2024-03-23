type Binding = {
	[key: number]: boolean;
};

type StatusPopupData = {
	tripPurposes: number[];
	departures: number[];
	arrivals: number[];
};

declare module '$lib/assets/*' {
	var meta;
	export default meta;
}
