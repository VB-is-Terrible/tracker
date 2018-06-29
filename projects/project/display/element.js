'use strict';

Elements.get('projects-Project');
{
const main = async () => {

await Elements.get('projects-Project');
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
		shadow.appendChild(template);
		this.applyPriorProperties('data');
	}
	get data() {
		return this.__data;
	}
	set data(value) {
		this.__data = value;
		this.shadowRoot.querySelector('.name').innerHTML = value.name;
		let status = value.status;
		let display = this.shadowRoot.querySelector('#status');
		let desc = this.shadowRoot.querySelector('p.desc');
		this.shadowRoot.querySelector('p.status').innerHTML = status.minor_code;
		requestAnimationFrame((e) => {
			desc.innerHTML = value.desc;
			if (status.minor === 0) {
				switch (status.major) {
					case 0:
						display.className = 'not_started';
						break;
					case 1:
						display.className = 'in_progress';
						break;
					case 2:
						display.className = 'finished';
						break;
					default:
						display.className = 'error';
				}
			} else {
				switch (status.minor) {
					case 1:
						display.className = 'awaiting';
						break;
					default:
						display.className = 'error';
				}
			}
		});
		if (this.data.required > 2) {
			let progress = this.shadowRoot.querySelector('p.progress');
			requestAnimationFrame((e) => {
				progress.innerHTML = this.data.progress.toString() + ' / ' +
				                     this.data.required.toString();
			});
		}

	}
};

Elements.load(Elements.elements.ProjectsProjectDisplay, 'elements-projects-project-display');
};

main();
}
