'use strict';

Elements.get();
{
const main = async () => {

await Elements.get();
/**
 * [ProjectsProjectMaker Description]
 * @augments Elements.elements.backbone2
 * @type {Object}
 */
Elements.elements.ProjectsProjectMaker = class ProjectsProjectMaker extends Elements.elements.backbone2 {
	constructor () {
		super();
		const self = this;

		this.name = 'ProjectsProjectMaker';
		const shadow = this.attachShadow({mode: 'open'});
		let template = Elements.importTemplate(this.name);

		//Fancy code goes here
		shadow.appendChild(template);
	}
};

Elements.load(Elements.elements.ProjectsProjectMaker, 'elements-projects-project-maker');
};

main();
}
