/* Javascript for PatientInteractionXBlock. */

var already_attempted = false;

function PatientInteractionXBlock(runtime, element) {
    function updateResult(result) {
	if (result["already_attempted"]) {
	    already_attempted = result["already_attempted"]
	    $(".doctor", element).each(function(index, elem) {
		$(elem).removeClass("selectable");
		if (index != result["given_answer"]) {
		    $(elem).addClass("not-selected");
		}
	    });
	    $(".result-icon").removeClass("icon-chat");
	    $(".result-icon").addClass(result.problem_solved? "icon-ok":"icon-cancel");
	    $(".pinteraction_block").addClass(result.problem_solved? "pblock-correct":"pblock-incorrect");
	    $(".patient-response").removeClass("hidden");
	    $(".patient-response").text(result["patient_answer"]);
	    $(".footer").removeClass("hidden");
	    $(".note").text(result["note"]);
	}
	//	$(".indicator").addClass(result.problem_solved? "icon-ok" : "icon-cancel");
    }

    var handlerUrl = runtime.handlerUrl(element, "check");

    $(".doctor", element).each(function(index, elem) {
	$(elem).click(function(eventObject) {
	    if (already_attempted) {
		return;
	    }
	    $.ajax({
		type: "POST",
		url: handlerUrl,
		data: JSON.stringify({"answer": index}),
		success: updateResult
            });
	});
    });

    $(function ($) {
	$.ajax({
	    type: "POST",
	    url: handlerUrl,
	    data: JSON.stringify({"answer": -1}),
	    success: updateResult
	});
        /* Here's where you'd do things on page load. */
    });
}
