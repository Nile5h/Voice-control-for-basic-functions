import datetime
def save_conversation(req , res, time):
    date = date = datetime.date.today()
    with open("conversation.txt", "a") as f:
        if "error" in res.lower():
            res = res[:15]
        if req == "Start":
            f.write(f"--------------------{date} ___ {time}-------------------\n\n")
        elif res == "yeh, i am listening":
            f.write(f"---------------{time}-------------\nUser(req): {req}\n")
        else:
            f.write(f"----{time}-----\nUser(req): {req} \nGoogle (res): {res} \n\n\n")