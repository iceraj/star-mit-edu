'use strict';

if( typeof (scb.ui ) == 'undefined') {
	scb.ui = {};
}

scb.ui.AssignmentsView = function scb_ui_AssignmentsView(state) {
	var self = this;

	self.show = function() {
		var assignments = new scb.AssignmentList(state.context.master_model.assignments, state.context);
		window.assignments = assignments;
		var workarea = state.workarea;
		workarea.html(scb_assignments.main({
			t : state.context.master_model,
			assignments : assignments
		}));
	}
}