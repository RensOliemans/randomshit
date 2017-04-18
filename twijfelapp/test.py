import data
import users

rens = users.RegularUser("rens")
henk = users.RegularUser("henk")
admin = users.AdminUser("admin", "abcde")

quest = data.Question("Yes or no?", ("yes", "no"), rens)
rens.add_question(quest)

quest.answer("yes", henk)
quest.report("invalid", henk)

print(rens)
print(admin)
