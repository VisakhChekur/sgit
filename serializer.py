class GitSerializer:

    SPACE = b' '
    NEWLINE = b'\n'
    SPACE_INT = ord(' ')
    MESSAGE_KEY = b''

    @staticmethod
    def deserialize(raw_data: bytes) -> dict[bytes, bytes]:
        """Parses according the following specification:
        
        1. Each key-value pair is separated by a space.
        2. Value of each value may span multiple lines in which case the
        continuation lines will have a space following the newline marker, '\n'
        which must be dropped by the parser.
        3. The beginning of a new key value pair is denoted by a newline
        marker WITHOUT being followed by a space.
        4. If a newline appears before a space or there's no space at all, then
        that implies the start of the message.
        """

        data: dict[bytes, bytes] = {}
        start: int = 0

        while True:

            
            key_end = raw_data.find(GitSerializer.SPACE, start)
            value_start = raw_data.find(GitSerializer.NEWLINE, start)

            # Number 4 in the specification
            if key_end < 0 or value_start < key_end:
                # Need the +1 to ignore the '\n' before
                # the start of the message
                data[GitSerializer.MESSAGE_KEY] = raw_data[value_start+1:]
                return data
            
            # Getting the key value
            key = raw_data[start: key_end]

            # Finding the entirety of the value by looking for the
            # first newline marker WITHOUT being followed by a space
            value: list[bytes] = []
            value_start = key_end + 1
            while True:
                value_end = raw_data.find(GitSerializer.NEWLINE, value_start)
                if raw_data[value_end+1] != GitSerializer.SPACE_INT:
                    # Not adding +1 to ignore the final '\n' that
                    # marks the end of the value
                    value.append(raw_data[value_start: value_end])
                    break
                value.append(raw_data[value_start: value_end + 1])
                # Need plus two to ignore the ' ' that follows the '\n'
                value_start = value_end + 2
            
            data[key] = b''.join(value)
            start = value_end + 1

    @staticmethod
    def serialize(data: dict[bytes, bytes]) -> bytes:

        serialized_bytes: list[bytes] = []

        # Getting all the key value pairs except the message
        for key, value in data.items():

            # Skipping the message
            if key == GitSerializer.MESSAGE_KEY:
                continue
            
            # 1 in the specification
            serialized_bytes.append(key)
            serialized_bytes.append(GitSerializer.SPACE)

            # Adding the value but changing all the '\n' to '\n '
            # i.e. adding a space after the '\n' to match 2 in the
            # specification
            values: list[bytes] = []
            value_start, newline = 0, value.find(GitSerializer.NEWLINE)
            while newline != -1:
                values.append(value[value_start: newline + 1])
                values.append(GitSerializer.SPACE)
                value_start = newline + 1
                newline = value.find(GitSerializer.NEWLINE, value_start)       

            values.append(value[value_start:])
            value = b''.join(values)
            serialized_bytes.append(value)

            # 3 in the specification
            serialized_bytes.append(GitSerializer.NEWLINE)

        # Adding the message
        serialized_bytes.append(GitSerializer.NEWLINE)
        serialized_bytes.append(data[GitSerializer.MESSAGE_KEY])
        
        print(b''.join(serialized_bytes))

        return b''.join(serialized_bytes)
