'use strict'

Elements.get('projects-Project', 'projects-project-display');
let data;
{
const main = async () => {
	let request = Elements.request('/start');
	await Elements.get('projects-Project');
	let json = await request;
	data = Projects.System.fromJSON(json);
	for (let project of data.projects) {
		let display = document.createElement('elements-projects-project-display');
		display.data = project;
		document.body.append(display);
	}
}

main();
}
