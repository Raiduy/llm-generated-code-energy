

def decimal_to_binary(decimal, padding_length):
    if not isinstance(decimal, int) or not isinstance(padding_length, int):
        return 'Invalid Input'
    if decimal < 0 or padding_length < 0:
        return 'Invalid Input'
    binary = bin(decimal)[2:]
    if len(binary) > padding_length:
        return 'Padding length is too small'
    padded_binary = binary.zfill(padding_length)
    return f'db{padded_binary}db'

if __name__ == '__main__':
    inputs = [eval(f"[{i}]") for i in ['15, 5', '32, 5', '32, 10', '0, 5', '1, 1', '255, 8', '1024, 5', '500, 10', '1023, 10', '-10, 2', '10, -2', '10, 0', '"string", 5', '10, "string"', '0.5, 1', 'True, 1', '10, True', '1, 1', '2, 2', '7, 3', '100, 7', '255, 8', '1023, 10', '2047, 11', '0, 1', '31, 1', '200, 4', '999, 20', '-5, 10', '10, -5', '"abc", 10', '10, "def"', 'None, 10', '10, None', '[], 10', '10, []', '{}, 10', '10, {}', '0, 5', '1, 1', '2, 1', '32, 6', '128, 8', '255, 8', '500, 10', '-1, 5', '15, -1', '"15", 5', '15, "5"', 'None, 5', '15, None', '0, 5', '1, 5', '255, 8', '1023, 10', '1000, 20', '150, 12', '-5, 5', '15, -5', '"15", 5', '15, "5"', '[], 5', '15, []', '0, 5', '1, 2', '2, 2', '10, 2', '10, 5', '255, 10', '255, 15', '1024, 20', '123456, 20', '-1, 5', '15, -1', '15, 0', "'15', 5", "15, '5'", 'True, 5', 'None, 5', '5.5, 5', '5, 5.5', '[15], 5', '15, [5]']]
    i = 0

    while(True):
        decimal_to_binary(*inputs[i%len(inputs)])
        i += 1

