def get_span(orig: str, new: str, editType: str):
    orig_list = orig.split()
    new_list = new.split()

    flag = False
    if editType == "deletion":
        if len(orig_list) <= len(new_list):
            raise AssertionError("expected deletion but new is not shorter")
        diff = len(orig_list) - len(new_list)
        for i, (o, n) in enumerate(zip(orig_list, new_list)):
            if o != n:
                orig_span = [i, i + diff - 1]
                new_span = [max(i-1, 0), i]
                flag = True
                break

    elif editType == "insertion":
        if len(orig_list) >= len(new_list):
            raise AssertionError("expected insertion but new is not longer")
        diff = len(new_list) - len(orig_list)
        for i, (o, n) in enumerate(zip(orig_list, new_list)):
            if o != n:
                new_span = [i, i + diff - 1]
                orig_span = [max(i-1, 0), i]
                flag = True
                break

    elif editType == "substitution":
        new_span = []
        orig_span = []
        for i, (o, n) in enumerate(zip(orig_list, new_list)):
            if o != n:
                new_span = [i]
                orig_span = [i]
                break
        if not new_span:
            raise AssertionError("no substitution found")
        for j, (o, n) in enumerate(zip(reversed(orig_list), reversed(new_list))):
            if o != n:
                new_span.append(len(new_list) - j - 1)
                orig_span.append(len(orig_list) - j - 1)
                flag = True
                break
    else:
        raise RuntimeError(f"editType unknown: {editType}")

    if not flag:
        raise RuntimeError(f"wrong editing with the specified edit type: original={orig} new={new} editType={editType}")

    return orig_span, new_span
