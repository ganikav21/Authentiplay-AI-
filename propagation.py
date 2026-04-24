def generate_path(similarity, age_hours):

    if similarity > 80 and age_hours < 2:
        return ["YouTube", "Telegram", "Pirate Sites", "Users"]

    elif similarity > 60:
        return ["YouTube", "Mirror Upload", "Users"]

    else:
        return ["YouTube"]