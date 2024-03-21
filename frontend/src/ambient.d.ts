type Binding = {
	[key: number]: boolean;
};

declare module '$lib/assets/*' {
	var meta;
	export default meta;
}
