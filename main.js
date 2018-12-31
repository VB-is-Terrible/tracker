'use strict'

Elements.get('projects-Project', 'projects-project-display',
             'drag-body', 'drag-element', 'projects-project-maker');
let DATA;
{
const main = async () => {
	let request = Elements.request('/start');
	await Elements.get('projects-Project');
	let json = await request;
	DATA = Projects.System.fromJSON(json);
	let projects = document.querySelector('#projects');
	for (let project_id of DATA.projects.keys()) {
		let display = document.createElement('elements-projects-project-display');
		display.data = DATA.get_event_by_id(project_id);
		projects.append(display);
	}
	console.log('done');
}

main();
}
