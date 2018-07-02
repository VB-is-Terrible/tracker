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
			display.className = 'border';
			if (status.minor === 0) {
				switch (status.major) {
					case 0:
						display.classList.add('not_started');
						break;
					case 1:
						display.classList.add('in_progress');
						break;
					case 2:
						display.classList.add('finished');
						break;
					default:
						display.classList.add('error');
				}
			} else {
				switch (status.minor) {
					case 1:
						display.classList.add('awaiting');
						break;
					default:
						display.classList.add('error');
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
