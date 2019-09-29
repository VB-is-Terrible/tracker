'use strict'

Elements.get('projects-Project', 'projects-project-full');

{
const get_project_id = () => {
	let page_locations = window.location.pathname.split('/');
	return parseInt(page_locations[page_locations.length - 1]);
}

const main = async () => {
	let request = Elements.request('../start');
	await Elements.get('projects-Project');
	let json = await request;
	Projects.main_project = Projects.System.fromJSON(json);
	let projects = document.querySelector('#a');
	let page_id = get_project_id();
	const current_project = Projects.main_project.get_event_by_id(page_id);
	projects.data = current_project;
	document.querySelector('title').innerHTML = current_project.name;
	console.log('done');
};

main();
}
