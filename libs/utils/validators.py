def is_valid_zip(zc):
    if len(zc) < 5:
        return False
    if not zc.isnumeric():
        return False
    return True