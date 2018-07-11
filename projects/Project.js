'use strict'

/**
 * @event Projects.Project#update
 * @type {Object}
 * @property {String} target Name of property changed
 */

/**
 * Interface for display of a Projects.Project
 * @interface ProjectDisplay
 */
/**
 * @function update
 * @description Fired upon a change event
 * @name ProjectDisplay.update
 * @param {Projects.Project#update} event Event been fired
 */

/**
 * Project namespace
 * @namespace Projects
 */
Projects = {
	ProjectParseError: class extends Error {
		constructor (...args) {
			super(...args);
			Error.captureStackTrace(this, this.constructor);
		}
	},
	STATUS_CODES_MAJOR: {
		0: 'Not started',
		1: 'In progress',
		2: 'Completed',
		'-1': 'Unknown status',
	},
	STATUS_CODES_MINOR: {
		0: null,
		1: 'Awaiting dependencies',
	},
	MAX_STATUS: 2,
	PROGRESS_STATUS: 1,
	Status: class Status {
		constructor (major, minor = 0) {
			this.major = major;
			this.minor = minor;
		}
		get major_code () {
			return Projects.STATUS_CODES_MAJOR[this.major];
		}
		get minor_code () {
			if (this.minor !== 0) {
				return Projects.STATUS_CODES_MINOR[this.minor];
			} else {
				return this.major_code;
			}
		}
	},
	Project: class Project {
		constructor (system, name, id, desc = '', required = 2) {
			this._system = system;
			this._name = name;
			this._desc = desc;
			this._dependencies = [];
			this.id = id;
			this._required = required;
			this._progress = 0;
			this._meta = 0;
			this._displays = new Set();
		}
		get name () {
			return this._name;
		}
		set name (value) {
			this._name = value;
			this.dispatchUpdate();
		}
		get desc () {
			return this._desc;
		}
		set desc (value) {
			this._desc = value;
			this.dispatchUpdate();
		}
		get dependencies () {
			return this._dependencies;
		}
		set dependencies (value) {
			this._dependencies = value;
			this.dispatchUpdate();
		}
		get required () {
			return this._required;
		}
		set required (value) {
			this._required = value;
			this.dispatchUpdate();
		}
		get progress () {
			return this._progress;
		}
		set progress (value) {
			this._progress = value;
			this.dispatchUpdate();
		}
		get meta () {
			return this._meta;
		}
		set meta (value) {
			this._meta = value;
			this.dispatchUpdate();
		}
		dispatchUpdate () {

		}
		addDisplay (display) {
			this._displays.add(display);
		}
		removeDisplay (display) {
			this._displays.delete(display);
		}
		_check_depends () {
			let progress = 0
			let completed = true;
			for (let depend of this.dependencies) {
				let project = this._system.get_event_by_id(depend);
				if (project.status.major !== Projects.MAX_STATUS) {
					completed = false;
				}
				progress = Math.max(progress, project.status.major);
			}
			if (completed) {
				return new Projects.Status(Projects.MAX_STATUS);
			} else if (progress > 0) {
				return new Projects.Status(0);
			} else {
				return new Projects.Status(-1);
			}
		}
		get status() {
			if (this.meta === 0) {
				if (this.progress === 0) {
					let status = this._check_depends();
					if (status.major === Projects.MAX_STATUS) {
						return new Projects.Status(0, 1);
					} else {
						return new Projects.Status(0, 0);
					}
				} else if (this.progress < this.required) {
					return new Projects.Status(Projects.PROGRESS_STATUS);
				} else {
					return new Projects.Status(Projects.MAX_STATUS);
				}

			}
		}
		get status_code() {
			return this.status.minor_code;
		}
		static fromJSONObj(obj, system) {
			if (obj.type !== 'Project') {
				throw new Projects.ProjectParseError('Not a Project representation');
			}
			let project = new this(system, obj.name, obj.id, obj.desc, obj.required);
			project.dependencies = obj.dependencies;
			project.progress = obj.progress;
			project.meta = obj.meta;
			return project
		}
	},
	System: class System {
		constructor() {
			this.projects = new Map();
		}
		static fromJSON(json) {
			return this.fromJSONObj(JSON.parse(json))
		}
		static fromJSONObj(obj) {
			if (obj.type !== 'System') {
				throw new Projects.ProjectParseError('Not a System');
			}
			let system = new Projects.System();
			for (let project_key in obj.projects) {
				let projectObj = obj.projects[project_key]
				let project = Projects.Project.fromJSONObj(projectObj, system);
				system.projects.set(project.id, project);
			}
			return system;
		}
		get_event_by_id (id) {
			return this.projects.get(id);
		}
	}
}

Elements.loaded('projects-Project');
