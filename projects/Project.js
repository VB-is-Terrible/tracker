
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
			this.system = system;
			this.name = name;
			this.desc = desc;
			this.dependencies = [];
			this.id = id;
			this.required = required;
			this.progress = 0;
			this.meta = 0;
		}
		_check_depends () {
			let progress = 0
			let completed = true;
			for (let depend of this.dependencies) {
				let project = this.system.get_event_by_id(depend);
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
	}
	System: class System {
		constructor() {
			this.projects = [];
		}
		static fromJSON(json) {
			return this.fromJSONObj(JSON.parse(json))
		}
		static fromJSONObj(obj) {
			if (obj.type !== 'System') {
				throw new Projects.ProjectParseError('Not a System');
			}
			let system = new Projects.System();
			for (let projectObj of obj.projects) {
				system.projects.push(project);
				let project = Projects.Project.fromJSONObj(projectObj, system);
			}

			return system;
		}
		get_event_by_id (id) {
			return this.projects.get(id);
		}
	}
}
