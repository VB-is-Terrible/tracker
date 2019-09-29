'use strict'

Elements.get('projects-Project', 'projects-project-display',
             'drag-body', 'drag-element', 'projects-project-maker', 'projects-project-editor');

{
const main = async () => {
	let request = Elements.request('/start');
	await Elements.get('projects-Project', 'drag-element');
	let json = await request;
	Projects.main_project = Projects.System.fromJSON(json);
	let projects = document.querySelector('#projects');
	for (let project_id of Projects.main_project.projects.keys()) {
		let display = document.createElement('elements-projects-project-display');
		display.data = Projects.main_project.get_event_by_id(project_id);
		projects.append(display);
	}
	console.log('done');
};

main();
}
