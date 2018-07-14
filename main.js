'use strict'

Elements.get('projects-Project', 'projects-project-display',
             'drag-body', 'drag-element', 'projects-project-maker');
let data;
{
const main = async () => {
	let request = Elements.request('/start');
	await Elements.get('projects-Project');
	let json = await request;
	data = Projects.System.fromJSON(json);
	let projects = document.querySelector('#projects');
	for (let project_id of data.projects.keys()) {
		let display = document.createElement('elements-projects-project-display');
		display.data = data.get_event_by_id(project_id);
		projects.append(display);
	}
        document.querySelector('elements-projects-project-maker').database = data;
	console.log('done');
}

main();
}
