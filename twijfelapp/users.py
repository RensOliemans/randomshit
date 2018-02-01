import data
from errors import OtherUserError


class User(object):
    """
    ``User`` object, superclass of RegularUser and AdminUser

    :arg str username:
        The username of the new user.
    """

    def __init__(self, username):
        """
        Creates a user with a username.

        :arg str username:
            The username of the new user.
        """
        if not isinstance(username, str):
            raise ValueError(
                "Invalid username. Should be string, was {0}"
                .format(type(username)))
        self.username = username
        self.admin = False

    def __str__(self):
        return "User: {0}".format(self.username)

    def __eq__(self, other):
        """
        Whether the user and another user are the same.
        """
        return self.username == other.username

    def is_admin(self):
        return self.admin


class RegularUser(User):
    """
    ``RegularUser`` object, child of ``User``. This user can
    ask and answer questions.

    :arg str username:
        The username of the new user.
    """

    def __init__(self, username):
        User.__init__(self, username)
        self.questions = list()

    def __str__(self):
        return "User: {0} \n{1}".format(self.username, self.questions
                                        if len(self.questions) > 0 else "")

    def __repr__(self):
        return self.username

    def add_question(self, question):
        assert isinstance(question, data.Question)
        if not question.user == self:
            raise OtherUserError(
                "User that owns the question: {0}. User that "
                "added the question: {1}. They have to be the same."
                .format(repr(question.user), repr(self))
            )
        self.questions.append(question)


class AdminUser(User):
    """
    ``AdminUser`` object, child of ``User``. This user can
    remove questions and remove users.

    :arg str username:
        The username of the admin user
    :arg str admincode:
        The admincode of the admin user
    """
    def __init__(self, username, admincode):
        pass

    def remove_user(self, user_to_remove):
        # assert admincode is valid
        pass
