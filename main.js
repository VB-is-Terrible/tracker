'use strict'

Elements.get('projects-Project', 'projects-project-display',
             'drag-body', 'drag-element', 'projects-project-maker');
let Data;
{
const main = async () => {
	let request = Elements.request('/start');
	await Elements.get('projects-Project');
	let json = await request;
	Data = Projects.System.fromJSON(json);
	let projects = document.querySelector('#projects');
	for (let project_id of Data.projects.keys()) {
		let display = document.createElement('elements-projects-project-display');
		display.data = Data.get_event_by_id(project_id);
		projects.append(display);
	}
	console.log('done');
}

main();
}
