/* Javascript for PatientInteractionXBlock. */

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
	    $(".result-icon", element).removeClass("icon-chat");
	    $(".result-icon", element).addClass(result.problem_solved? "icon-ok":"icon-cancel");
	    $(".pinteraction_block", element).addClass(result.problem_solved? "pblock-correct":"pblock-incorrect");
	    $(".patient-response", element).removeClass("hidden");
	    $(".patient-response", element).text(result["patient_answer"]);
	    $(".footer", element).removeClass("hidden");
	    $(".note", element).text(result["note"]);
	}
	//	$(".indicator").addClass(result.problem_solved? "icon-ok" : "icon-cancel");
    }

    var handlerUrl = runtime.handlerUrl(element, "check");

    $(".doctor", element).each(function(index, elem) {
	$(elem).click(function(eventObject) {
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
