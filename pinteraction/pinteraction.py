"""
XBlock to do patient interaction questions, i.e. what is the
appropiate reaction to a given patient question or statement
"""

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Boolean, String, Scope
from xblock.fragment import Fragment

def resource_string(path):
    """Handy helper for getting resources from our kit."""
    data = pkg_resources.resource_string(__name__, path)
    return data.decode("utf8")

class PatientInteractionXBlock(XBlock):
    """
    Ask a question along a number of possible answers. When an answer
    is clicked, show what the patient might answer and whether the
    chosen answer was correct
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    name = String(help="Name of this xblock", scope=Scope.content, default="Patient interaction")
    question = String(help="The question", scope=Scope.content, default="")
    correct_answer = Integer(help="Correct answer of this question", scope=Scope.content, default=0)
    problem_attempted = Boolean(help="Has the student attempted this problem?", scope=Scope.user_state, default=False)
    given_answer = Integer(help="The answer the student has given", scope=Scope.user_state, default=-1)
    has_children = True
    has_score = True
    icon_class = "problem"

    @classmethod
    def parse_xml(cls, node, runtime, keys, id_generator):
        block = runtime.construct_xblock_from_class(cls, keys)
        for child in node:
            block.runtime.add_node_as_child(block, child, id_generator)

        # Attributes become fields.
        for name, value in node.items():  # lxml has no iteritems
            cls._set_field_if_present(block, name, value, {})

        text = node.text
        if text:
            text = text.strip()
            if text:
                block.question = text
        return block

    def student_view(self, context=None):
        """
        The primary view of the PatientInteractionXBlock, shown to students
        when viewing courses.
        """
        result = Fragment()
        result.add_css(resource_string("static/css/pinteraction.css"))
        result.add_css(resource_string("static/css/icons.css"))
        child_frags = self.runtime.render_children(self, context=context)
        result.add_frags_resources(child_frags)
        result.add_content(self.runtime.render_template("pinteraction.html", children=child_frags, question=self.question, name=self.name))
        result.add_javascript(resource_string("static/js/src/pinteraction.js"))
        result.initialize_js('PatientInteractionXBlock')
        return result

    @XBlock.json_handler
    def check(self, data, suffix=''):
        """
        check if correct
        """
        print(data["answer"])
        if not self.problem_attempted and (int(data["answer"]) != -1):
            self.problem_attempted = True
            self.given_answer = int(data["answer"])
            event_data = {'value': 1 if self.given_answer == self.correct_answer else 0, 'max_value': 1}
            self.runtime.publish(self, 'grade', event_data)
        return {"problem_solved": self.given_answer == self.correct_answer,
                "given_answer": self.given_answer,
                "patient_answer": self.get_children()[self.given_answer].patient_response,
                "note":  self.get_children()[self.given_answer].instructor_note,
                "already_attempted": self.problem_attempted}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("PatientInteractionXBlock",
             """
             <pinteraction name="Interaktion" correct_answer='1'>
             Lorem ipsum dolor sit amet?
               <response doctor_response="consetetur sadipscing elitr" patient_response="sed diam nonumy eirmod tempor" instructor_note="Footszli"/>
               <response doctor_response="At vero eos et accusam" patient_response="sed diam nonumy" instructor_note="hutsli"/>
               <response doctor_response="Stet clita kasd gubergren" patient_response="invidunt ut labore et dolore magna aliquyam" instructor_note="brutsli"/>
             </pinteraction>
             """),
            ("MultiPatientInteractionXBlock",
             """
             <vertical_demo>
             <pinteraction correct_answer='0'>
             You rock
               <response doctor_response="Lorem Ipsum" patient_response="Dolor"/>
               <response doctor_response="Foo Bar" patient_response="Baz"/>
               <response doctor_response="Foo Bus" patient_response="Bla"/>
             </pinteraction>
             <pinteraction correct_answer='1'>
             You rock
               <response doctor_response="Lorem Ipsum" patient_response="Dolor"/>
               <response doctor_response="Foo Bar" patient_response="Baz"/>
               <response doctor_response="Foo Bus" patient_response="Bla"/>
             </pinteraction>
             <pinteraction correct_answer='2'>
             You rock
               <response doctor_response="Lorem Ipsum" patient_response="Dolor"/>
               <response doctor_response="Foo Bar" patient_response="Baz"/>
               <response doctor_response="Foo Bus" patient_response="Bla"/>
             </pinteraction>
             </vertical_demo>
             """),
        ]

class PResponseXBlock(XBlock):
    doctor_response = String(help="The response of the doctor", scope=Scope.content, default="")
    patient_response = String(help="The response of the patient", scope=Scope.content, default="")
    instructor_note = String(help="Additional note of the instructor", scope=Scope.content, default="")

    def student_view(self, context=None):
        html = resource_string("static/html/response.html")
        frag = Fragment(html.format(self=self))
        return frag
