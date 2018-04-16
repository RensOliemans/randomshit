import time
import users


class Question():
    """
    The ``Question`` class
    """

    def __init__(self, title, answers, user):
        self.title = title
        self.answers = answers
        if not isinstance(user, users.RegularUser):
            raise AssertionError()
        self.user = user
        self.date = time.strftime("%x")

        self.answered = False
        self.chosen_answer = None
        self.answer_user = None
        self.answer_date = None

        self.reported = False
        self.report_reason = None
        self.report_user = None
        self.report_date = None

    def __str__(self):
        """
        Returns a string representation of the object if you call
        ``print(question)``.
        """
        answered = "Not answered yet."
        if self.answered:
            answered = "Answered by: {0}. Answer chosen: \"{1}\", on {2}."
            answered = answered.format(repr(self.answer_user),
                                       self.chosen_answer, self.answer_date)
        reported = "Not reported yet."
        if self.reported:
            reported = "Reported by: {0} on {1}, reason: \"{2}\""
            reported = reported.format(repr(self.report_user),
                                       self.report_date, self.report_reason)
        result = "Question: '{0} {1} {2}'"
        result = result.format(self.title, answered, reported)
        return result

    def __repr__(self):
        """
        Returns the representation of a ``Question`` object if you call
        ``repr(question)``.
        """
        return self.__str__()

    def answer(self, answer, answer_user):
        """
        Answers the question.

        :arg str answer:
            Answer that has been chosen.

        :arg RegularUser answer_user:
            User that answered the question.
        """
        if answer not in self.answers:
            raise AssertionError("Answer is not in possible answers")
        self.answered = True
        self.chosen_answer = answer
        self.answer_user = answer_user
        self.answer_date = time.strftime("%x")

    def report(self, report_reason, report_user):
        """
        Reports the question.

        :arg str report_reason:
            Reason of report.

        :arg User report_user:
            User that reports the question.
        """
        # assert report_user exists
        self.reported = True
        self.report_reason = report_reason
        self.report_user = report_user
        self.report_date = time.strftime("%x")
