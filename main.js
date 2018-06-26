'use strict'

Elements.get('projects-Project', 'projects-project-display');
let data;
{
const main = async () => {
	let json = Elements.request('/start');
	await Elements.get('projects-Project');
	data = Projects.System.fromJSONObj(json);
	for (let project of data.projects) {
		let display = document.createElement('elements-projects-project-display');
		display.data = project;
		document.body.append(display);
	}
}

main();
}
