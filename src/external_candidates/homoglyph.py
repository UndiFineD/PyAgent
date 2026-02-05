class CharacterManager:
    def __init__(self):
        self.chars_to_sets = {}

    def add_pair(self, a, b):
        a_set = self.get_set_for_char(a)
        b_set = self.get_set_for_char(b)

        if a_set and b_set:
            if a_set is b_set:
                return
            else:
                a_set.update(b_set)
                for b_member in list(b_set):
                    self.chars_to_sets[b_member] = a_set

        elif a_set:
            a_set.add(b)
            self.chars_to_sets[b] = a_set

        elif b_set:
            b_set.add(a)
            self.chars_to_sets[a] = b_set

        else:
            s = set([a, b])
            self.chars_to_sets[a] = s
            self.chars_to_sets[b] = s

    def get_set_for_char(self, c):
        return self.chars_to_sets.get(c)

    def get_list_of_sets(self):
        l = []
        for s in map(sorted, set(map(tuple, self.chars_to_sets.values()))):
            if s not in l:
                l.append(s)
        return sorted(l)
