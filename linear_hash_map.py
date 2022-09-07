class HashMap:
    """Simple linear probing hashmap with resizing"""

    def __init__(self, *args, array_size=8):
        self._array_size = max(2, array_size if array_size %
                               2 == 0 else array_size + 1)
        self._array = [None for item in range(self._array_size)]
        self._item_count = 0

    @property
    def _is_full(self) -> bool:
        return self._item_count == self._array_size - 1

    def _hash(self, key: str) -> int:
        # Very basic - would need a better hasher for large maps
        return sum(key.encode()) % self._array_size

    def _get_index_and_entry_for(self, key: str):
        index = self._hash(key)
        array_entry = self._array[index]
        loop_count = 0

        while(array_entry is not None and array_entry[0] != key):
            # Probing by (hash + hash) / +1 to reduce clustering
            if loop_count == 0:
                index += index
            else:
                index += 1
            index = index % self._array_size
            array_entry = self._array[index]
            loop_count += 1

        return index, array_entry

    def _not_None_entries(self):
        return filter(lambda e: e is not None, self._array)

    def _resize(self):
        self._array_size = int(self._array_size * 1.5)
        current_entries = self._not_None_entries()
        self._array = [None for _ in range(self._array_size)]
        self._item_count = 0
        for key, value in current_entries:
            self[key] = value

    def __setitem__(self, key: str, value):
        if self._is_full:
            self._resize()

        index, entry = self._get_index_and_entry_for(key)
        if entry is None:
            self._item_count += 1
        self._array[index] = [key, value]

    def __getitem__(self, key: str):
        _, entry = self._get_index_and_entry_for(key)
        return None if entry is None else entry[1]

    def __delitem__(self, key: str):
        index, entry = self._get_index_and_entry_for(key)
        if entry is not None:
            self._item_count -= 1
        self._array[index] = None

    def __len__(self):
        return self._item_count

    def __repr__(self):
        repr_str = "{ "
        for key, value in self._not_None_entries():
            repr_str += f"{key.__repr__()}: {value.__repr__()}, "
        repr_str = repr_str[:-2]
        repr_str += " }"
        return repr_str


def main():
    values = [
        ['ab', 'a'],
        ['aaaa', 'b'],
        ['aba', 'c'],
        ['abcd', 'e']]

    print("Create HashMap: HashMap(array_size=3)")
    map = HashMap(array_size=3)

    print(f"Add {values =}")
    for key, value in values:
        map[key] = value
    print(f"Can print map: {map = }")
    print(f"Map resized: {len(map) == 3 = }")
    print(f"Map gets correctly : {map['ba'] == None = }")
    print(f"Map gets correctly : {map['aaaa'] == 'b' = }")
    print("Map setter: map['ba'] = 'f'")
    map['ba'] = 'f'
    print(f"Map sets correctly: {map['ba'] == 'f' = }")
    print(f"Map size is updated correctly: {len(map) = }")
    print("Map can delete items: del map['ab']}")
    del map['ab']
    print(f"{len(map) = }")
    print(f"{map['ab'] = }")
    print(f"{map = }")


if __name__ == "__main__":
    main()
