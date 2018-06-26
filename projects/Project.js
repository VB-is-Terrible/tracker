
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
		static fromJSONObj(obj) {
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
	}
}
