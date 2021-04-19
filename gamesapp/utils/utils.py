def list_to_str(using, list_):
    string = ""
    for i, item in enumerate(list_):
        if i != len(list_) - 1:
            string += f'{item}' + using
        else:
            string += f'{item}'

    return string


def split_platforms(platforms):
    aux = platforms.copy()
    for platform in aux:
        stripped_platform = platform.strip()
        if len(stripped_platform) == 0 or stripped_platform == '/':
            platforms.remove(platform)

    for i, platform in enumerate(platforms):
        platforms[i] = platform.strip()

    return platforms


def split_tags(tags):
    aux = tags.copy()
    for tag in aux:
        if len(tag.strip()) == 0:
            tags.remove(tag)

    return tags
