// This file was automatically generated from assignments.soy.
// Please don't edit this file by hand.

if (typeof scb_assignments == 'undefined') { var scb_assignments = {}; }


scb_assignments.main = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<div class=\'assignments_selector\'>');
  scb_assignments.display_title(opt_data, output);
  scb_assignments.display_description(opt_data, output);
  scb_assignments.display_assignments(opt_data, output);
  output.append('</div>');
  return opt_sb ? '' : output.toString();
};


scb_assignments.display_title = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<div class=\'assignments_title assignments_block\'>', soy.$$escapeHtml(opt_data.t.app_title), '</div>');
  return opt_sb ? '' : output.toString();
};


scb_assignments.display_description = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<div class=\'assignments_description assignments_block\'>', opt_data.t.app_description, '</div>');
  return opt_sb ? '' : output.toString();
};


scb_assignments.display_assignments = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  output.append('<div class=\'assignement_assignments_list assignments_block\'><dl>');
  var assignmentList22 = opt_data.assignments.list;
  var assignmentListLen22 = assignmentList22.length;
  for (var assignmentIndex22 = 0; assignmentIndex22 < assignmentListLen22; assignmentIndex22++) {
    var assignmentData22 = assignmentList22[assignmentIndex22];
    output.append('<dt class=\'assignement_assignement_name\'><a href=\'#\' model_id=\'', soy.$$escapeHtml(assignmentData22.id), '\' class=\'select_assignement\'>', soy.$$escapeHtml(assignmentData22.name), '</a></dt><dd class=\'assignement_assignement_description\'>', assignmentData22.description, '</dd>');
    scb_assignments.display_experiments({experiments: assignmentData22.experiments, assignment: assignmentData22}, output);
  }
  output.append('</dl></div>');
  return opt_sb ? '' : output.toString();
};


scb_assignments.display_experiments = function(opt_data, opt_sb) {
  var output = opt_sb || new soy.StringBuilder();
  if (opt_data.experiments.list.length != 0) {
    output.append('<ul class=\'assignement_experiment_list\'>');
    var experimentList40 = opt_data.experiments.list;
    var experimentListLen40 = experimentList40.length;
    for (var experimentIndex40 = 0; experimentIndex40 < experimentListLen40; experimentIndex40++) {
      var experimentData40 = experimentList40[experimentIndex40];
      output.append('<li class=\'assignement_experiment_list_item\'><a class=\'select_assignement_experiment\' href=\'#\' model_id=\'', soy.$$escapeHtml(opt_data.assignment.id), '\' sub_model_id=\'', soy.$$escapeHtml(experimentData40.id), '\'>', soy.$$escapeHtml(experimentData40.name), '</a></li>');
    }
    output.append('</ul>');
  }
  return opt_sb ? '' : output.toString();
};
