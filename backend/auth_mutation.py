def resolve_login(_, info, username, password):
    request = info.context["request"]
    if username == "Austin" and password == "Pena":
        return True
    return False


def resolve_logout(_, info, username, password):
    return True
