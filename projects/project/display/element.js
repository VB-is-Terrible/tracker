'use strict';

Elements.get();
{
const main = async () => {

await Elements.get();
/**
 * [ProjectsProjectDisplay Description]
 * @augments Elements.elements.backbone2
 * @type {Object}
 */
Elements.elements.ProjectsProjectDisplay = class ProjectsProjectDisplay extends Elements.elements.backbone2 {
	constructor () {
		super();
		const self = this;

		this.name = 'ProjectsProjectDisplay';
		this.__data = null;
		const shadow = this.attachShadow({mode: 'open'});
		let template = Elements.importTemplate(this.name);

		//Fancy code goes here
		this.applyPriorProperties('data');
		shadow.appendChild(template);
	}
	get data() {
		return this.__data;
	}
	set data(value) {
		this.__data = value;
		this.shadowRoot.querySelector('#text').innerHTML = value.
	}
};

Elements.load(Elements.elements.ProjectsProjectDisplay, 'elements-projects-project-display');
};

main();
}
