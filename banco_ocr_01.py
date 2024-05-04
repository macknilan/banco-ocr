#
import csv
import itertools
from functools import reduce

template = [
    " _     _  _     _  _  _  _  _ ",
    "| |  | _| _||_||_ |_   ||_||_|",
    "|_|  ||_  _|  | _||_|  ||_| _|"
]

list_clock_number = [
    [
        " _ ",
        "| |",
        "|_|",
        "   "
    ],
    [
        "   ",
        "  |",
        "  |",
        "   "
    ],
    [
        " _ ",
        " _|",
        "|_ ",
        "   "
    ],
    [
        " _ ",
        " _|",
        " _|",
        "   "
    ],
    [
        "   ",
        "|_|",
        "  |",
        "   "
    ],
    [
        " _ ",
        "|_ ",
        " _|",
        "   "
    ],
    [
        " _ ",
        "|_ ",
        "|_|",
        "   "
    ],
    [
        " _ ",
        "  |",
        "  |",
        "   "
    ],
    [
        " _ ",
        "|_|",
        "|_|",
        "   "
    ],
    [
        " _ ",
        "|_|",
        " _|",
        "   "
    ]
]


def create_file():

    result = []

    # REALIZA EL SLICE DESDE CUARTO CARÁCTER DE CADA LINEA HASTA EL FINAÑ
    # Y ADICIONA LOS PRIMEROS 3 CARACTERES DE CADA LINEA AL FINAL
    try:
        for _ in range(500):
            for index, position in enumerate(range(30, -1, -3)):
                # SET EL VALOR ACTUAL DE LA POSICIÓN Y EL VALOR SIGUIENTE
                if index < len(range(30, -1, -3)) - 1:
                    next_position = range(30, -1, -3)[index + 1]

                    # print(f"{position}, {next_position}")

                    result.append([line[position:] + line[:next_position] for line in template])

        with open('result_clock_font.txt', 'w') as f:
            for sublist in result:
                for item in sublist:
                    f.write("%s\n" % item)
                f.write("                           ")
                f.write("\n")
    except Exception as e:
        return e

    return 200


def read_file():

    lines_clocking_font = []

    with open('result_clock_font.txt', 'r') as f:
        while True:
            line = list(itertools.islice(f, 4))
            if line:
                lines_clocking_font.append(line)
            else:
                break

        return lines_clocking_font


def save_digit_entrance_to_file(list_digit_number, filename):
    try:
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(list_digit_number)

    except Exception as e:
        return e

    return 200


def clock_font_to_digit(list_all_sequence):

    # print(list_all_sequence)
    list_digit_number = []
    list_position_number = [(0, 3), (3, 6), (6, 9), (9, 12), (12, 15), (15, 18), (18, 21), (21, 24), (24, 27)]

    for line_index, line in enumerate(list_all_sequence):  # COMPLETE LIST
        # print("NEW LINE")
        # print(line)
        list_garbage = []
        for pos_number in list_position_number:  # LIST OF POSITIONS IN THE LINE (9)

            for index, digit in enumerate(list_clock_number):  # LIST OF DIGITS CLOCK TYPE (10)

                if digit == [number[pos_number[0]:pos_number[1]] for number in line]:
                    # print(f"El número es: {index}")
                    list_garbage.append(index)

        list_digit_number.append(list_garbage)

    response = save_digit_entrance_to_file(list_digit_number, 'result_digits_numbers.csv')

    if response == 200:
        print("Archivo creado correctamente")
        return 200
    else:
        print(f"Error: {response}")


def utility_checksum_sum(x, y):
    return x + y


def checksum_calculation():

    checksum_set_params = [
        ("d9", 1), ("d8", 2), ("d7", 3), ("d6", 4), ("d5", 5), ("d4", 6), ("d3", 7), ("d2", 8), ("d1", 9)
    ]
    list_checksum_status = []
    try:
        with open('result_digits_numbers.csv', 'r') as f:
            reader = csv.reader(f)
            list_all_account_number = [[int(num) for num in row] for row in reader]

            for index_a, account_number in enumerate(list_all_account_number):
                list_garbage = []
                list_garbage_2 = []
                for index_b, digit in enumerate(account_number):
                    list_garbage_2.append(digit * checksum_set_params[index_b][1])
                pre_result = reduce(utility_checksum_sum, list_garbage_2)
                result = pre_result % 11
                if result == 0:
                    list_garbage.append("OK")
                else:
                    list_garbage.append("ERR")

                list_checksum_status.append(list_garbage)

        return list_checksum_status

    except Exception as e:
        return e





def save_checksum_sts_to_file(list_sts_check):

    try:
        # LEER EL ARCHIVO `result_digits_numbers.csv` CREADO ANTERIORMENTE
        with open('result_digits_numbers.csv', 'r') as f:
            reader = csv.reader(f)
            data = list(reader)

        # AGREGAR EL ESTADO DE LA VERIFICACIÓN DE CADA NÚMERO/LINEA DE CUENTA EL ARCHIVO AL FINAL
        for row, status in zip(data, list_sts_check):
            while len(row) < 10:
                row.append('')
            # LA LISTA DE STATUS ES UNA LISTA DE LISTAS, POR ESO SE TOMA EL PRIMER ELEMENTO DE LA LISTA
            row[9] = status[0]

        with open('result_digits_numbers.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    except Exception as e:
        return e

    return 200


if __name__ == "__main__":
    """
    TODO:
    """
    # CREAR EL ARCHIVO CON EL FORMATO DE LOS NÚMEROS DEL RELOJ
    file_created = create_file()
    if file_created == 200:
        print("Archivo creado correctamente")
    else:
        print(f"Error: {file_created}")

    # LEER EL ARCHIVO CREADO
    clocking_font_lines = read_file()

    # CONVERTIR EL FORMATO DE LOS NÚMEROS DEL RELOJ A NÚMEROS
    clock_font_to_digit(clocking_font_lines)

    # VERIFICACIÓN PARA CADA NUMERO DE CUENTA
    list_sts_check_sum = checksum_calculation()

    res = save_checksum_sts_to_file(list_sts_check_sum)
    print(res)
