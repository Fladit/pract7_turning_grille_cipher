import random
import copy
import math


def check_cell_identity(matrix: list, row_index: int, column_index: int, row_number: int, column_number: int):
    if (matrix[row_index][column_index] == False
            and matrix[row_index][column_number - column_index - 1] == False
            and matrix[row_number - row_index - 1][column_index] == False
            and matrix[row_number - row_index - 1][column_number - column_index - 1] == False
    ):
        return True
    else:
        return False


def reverse_template(template_matrix: list):
    for row in template_matrix:
        row.reverse()
    return template_matrix


def rotate_template_to_180_degree(template_matrix: list):
    template_matrix.reverse()
    for i in range(0, len(template_matrix)):
        template_matrix[i].reverse()
    return template_matrix


def encode_part_of_matrix_by_template(template_matrix, word, index, encode_matrix):
    for i in range(0, len(template_matrix)):
        for j in range(0, len(template_matrix[0])):
            if template_matrix[i][j]:
                encode_matrix[i][j] = word[index]
                index += 1
    return encode_matrix, index


def encode(template_matrix, word: str):
    word_corrected = word
    while len(word_corrected) < len(template_matrix) * len(template_matrix[0]):
        word_corrected += "-"
    encode_matrix = []
    current_index = 0

    for i in range(0, len(template_matrix)):
        row1 = []
        for j in range(0, len(template_matrix[0])):
            row1.append("-")
        encode_matrix.append(row1)

    '''Исходная решётка'''
    copy_of_temp_matrix = copy.deepcopy(template_matrix)
    encode_matrix, current_index = encode_part_of_matrix_by_template(copy_of_temp_matrix, word_corrected, current_index,
                                                                     encode_matrix)
    '''Исходная решётка, повёрнутая на 180 градусов'''
    copy_of_temp_matrix = rotate_template_to_180_degree(copy_of_temp_matrix)
    encode_matrix, current_index = encode_part_of_matrix_by_template(copy_of_temp_matrix, word_corrected, current_index,
                                                                     encode_matrix)
    '''Вертикальное отражение решётки, повёрнутой на 180 градусов'''
    copy_of_temp_matrix = reverse_template(copy_of_temp_matrix)
    encode_matrix, current_index = encode_part_of_matrix_by_template(copy_of_temp_matrix, word_corrected, current_index,
                                                                     encode_matrix)
    '''Вертикальной отражение исходной решётки'''
    copy_of_temp_matrix = rotate_template_to_180_degree(copy_of_temp_matrix)
    encode_matrix, current_index = encode_part_of_matrix_by_template(copy_of_temp_matrix, word_corrected, current_index,
                                                                     encode_matrix)
    return encode_matrix


def decode_part_of_encode_word(encode_word, key_matrix):
    decode_part = ""
    for i in range(0, len(key_matrix)):
        for j in range(0, len(key_matrix[0])):
            if key_matrix[i][j]:
                decode_part += encode_word[i][j]
    return decode_part


def decode(encode_word, key_matrix):
    decode_word = ""
    decode_word += decode_part_of_encode_word(encode_word, key_matrix)
    copy_key_matrix = copy.deepcopy(key_matrix)
    copy_key_matrix = rotate_template_to_180_degree(copy_key_matrix)
    decode_word += decode_part_of_encode_word(encode_word, copy_key_matrix)
    copy_key_matrix = reverse_template(copy_key_matrix)
    decode_word += decode_part_of_encode_word(encode_word, copy_key_matrix)
    copy_key_matrix = rotate_template_to_180_degree(copy_key_matrix)
    decode_word += decode_part_of_encode_word(encode_word, copy_key_matrix)
    return decode_word


def create_template(m: int, k: int):
    matrix_template = []
    matrix_possible = []
    row_number = m
    column_number = k
    for j in range(0, row_number):
        row = []
        for z in range(0, column_number):
            cell = [j, z]
            matrix_possible.append(cell)
            row.append(False)
        matrix_template.append(row)

    filled_cells = 0
    while filled_cells != ((m * k) / 4):
        random_cell = random.choice(matrix_possible)
        row_index = random_cell[0]
        column_index = random_cell[1]
        if check_cell_identity(matrix_template, row_index, column_index, row_number, column_number):
            matrix_template[row_index][column_index] = True
            filled_cells += 1
        matrix_possible.remove([row_index, column_index])
        matrix_possible.remove([row_index, column_number - column_index - 1])
        matrix_possible.remove([row_number - row_index - 1, column_index])
        matrix_possible.remove([row_number - row_index - 1, column_number - column_index - 1])
    return matrix_template


def factorization(size: int):
    multipliers = []
    for i in range(2, size, 2):
        if size % i == 0:
            multipliers.append(i)
    rand_multiplier = random.choice(multipliers)
    second_multiplier = size // rand_multiplier
    if second_multiplier % 2 == 1:
        second_multiplier += 1
    if rand_multiplier > second_multiplier:
        a = second_multiplier
        second_multiplier = rand_multiplier
        rand_multiplier = a
    return rand_multiplier, second_multiplier


def determine_size_of_matrix(word: str):
    word_len = len(word)
    if word_len % 2 == 1:
        word_len += 1
    return factorization(word_len)


word_str = "ШифрПоворотнаяРешётка"
word_str = word_str.upper()
print("Исходное слово: ", word_str)
m, k = determine_size_of_matrix(word_str)
matrix_template = create_template(m, k)
print("Ключ-решётка: (True - вырез трафарета)")
for i in matrix_template:
    print(i)
encode_matrix = encode(matrix_template, word_str)
print("\nМатрица с зашифрованным словом:")
for i in encode_matrix:
    print(i)
encode_word = ""
for row in encode_matrix:
    for letter in row:
        encode_word += letter
print("\nЗакодированное слово:", encode_word)
print("Процесс декодирования...")
decode_word = decode(encode_matrix, matrix_template)
print("Декодированное слово:", decode_word)

