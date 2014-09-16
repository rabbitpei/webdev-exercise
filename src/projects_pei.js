function Project(id, type, name, lastActivity) {
    this.id = id;
    this.type = type;
    this.name = name;
    this.lastActivity = lastActivity;
}

// The list of all projects currently in the system.
// (Feel free to imagine this came from a database somewhere on page load.)
var CURRENT_PROJECTS = [
    new Project(0, "Training", "Patrick's experimental branch", new Date(2014, 6, 17, 13, 5, 842)),
    new Project(1, "Testing", "Blind test of autosuggest model", new Date(2014, 6, 21, 18, 44, 229))
];

// The current maximum ID, so we know how to allocate an ID for a new project.
// (Yes, the database should be taking care of this, too.)
var MAX_ID = Math.max.apply(null, $.map(CURRENT_PROJECTS, function(pj) { return pj.id; }));

$(function(){
    var loadProjects = function($container, projects) {
        $.fn.append.apply($container, $.map(projects, function(pj) {
            return $("<tr>").append(
                $("<td>").text(pj.id),
                $("<td>").text(pj.type),
                $("<td>").text(pj.name),
                $("<td>").text(pj.lastActivity.toString()),
                $('<input type="button" value="check update" />').click(function(e){
				  	$.getJSON("https://api.github.com/repos/quixey/webdev-exercise/compare/baseline-branch..." + pj.name, function() {
				      alert("Querying if this project is up to date");
			        })
			          .done(function(data) {
				      	$.each(data, function (key, val) {
					      if (key == "status") {
						    alert ("status is " + val);
						 }
				        });
			        })
			          .fail(function() {
				        alert("Checking updated failed, please try again later.");
			        })
			          .always(function() {
				        e.preventDefault();
			        });
			    })
            );
        }));
    };

    // Creates a new project based on the user input in the form.
    var createProject = function($form) {
        return new Project(
            MAX_ID + 1,
            $form.find("#project-type").val(),
            $form.find("#project-name").val(),
            new Date()
        );
    };

    // Clears the data in the form so that it's easy to enter a new project.
    var resetForm = function($form) {
        $form.find("#project-type").val("");
        $form.find("#project-name").val("");
        $form.find("input:first").focus();
    };

    var $projectTable = $("#project-list>tbody");
    loadProjects($projectTable, CURRENT_PROJECTS);

    $("#add-project-form").submit(function(e) {
        var $form = $(this);
        pj = createProject($form);
        if (!pj.type) {
	      alert("can't create a project with empty type!");
	      return;
        }
        if (!pj.name) {
	      alert("can't create a project with empty name");
	      return;
        }
        $.get("https://api.github.com/repos/quixey/webdev-exercise/branches/" + pj.name, function() {
	      alert("Querying if this project exists in Github!");
        })
          .done(function() {
	      	MAX_ID = pj.id;
	        CURRENT_PROJECTS.push(pj);
	        loadProjects($projectTable, [pj]);
        })
          .fail(function() {
	        alert("Didn't find the project in Github, please reenter the info!");
        })
          .always(function() {
	        resetForm($form);
	        e.preventDefault();
        });
    });

});
