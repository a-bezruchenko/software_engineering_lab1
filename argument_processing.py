# encoding: utf-8
import argparse
import os.path
import math

from typing import List

# разбирает аргументы командной строки
def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("data_len", type=int, help="количество генерируемых данных: чисел или букв")
    parser.add_argument("output_path", nargs='?', help="файл, в который сохранять вывод")
    parser.add_argument("-seed", default=0, type=int, help="зерно для ГСЧ")
    parser.add_argument("-type", "-t", default = "int", choices=['int', 'float', 'str'],  help="тип генерируемых данных: int, float или str")
    parser.add_argument("-distribution", "-d", choices=['uniform', 'normal'], help="тип распределения: uniform или normal")
    parser.add_argument("-mean", type=float, help="матожидание распределения")
    parser.add_argument("-std", type=float, help="стандартное отклонение распределения")
    parser.add_argument("-min_value", "-min",type=float, help="нижняя граница распределения")
    parser.add_argument("-max_value", "-max", type=float, help="верхняя граница распределения")
    parser.add_argument("-charset", "-c", help="набор символов, из которых берутся символы для генерации")
    parser.add_argument("--timeit", action="store_true", help="если указан, то замеряет и выводит в консоль время работы")
    args = parser.parse_args(arguments)
    return args

# проверяет на корректность аргументы командной строки
# ничего не возвращает, но кидает исключение при ошибке
# Q: может, было б правильнее возвращать статус проверки и строку с ошибкой, но это было б неудобнее использовать в main
def validate_arguments(parsed_arguments: argparse.Namespace):
    # проверка существования папки для выходного файла, если он указан
    if parsed_arguments.output_path is not None:
        output_folder = os.path.dirname(os.path.normpath(parsed_arguments.output_path))
        if not os.path.isdir(output_folder):
            raise ValueError("Folder " + output_folder + " doesn't exist")

    # проверка совместимости параметров
    # проверка параметров, не зависящих от распределения
    if parsed_arguments.type == "str" and parsed_arguments.distribution is not None:
        raise ValueError( "'str' data type incompatible with -distribution argument")
    if parsed_arguments.type in ["int", "float"] and parsed_arguments.distribution is None:
        raise ValueError( "Need -distribution argument to generate types 'int' and 'float' data")
    if parsed_arguments.type != "str" and parsed_arguments.charset is not None:
        raise ValueError("-charset argument is only compatible with 'str' data type")

    # проверка параметров, зависящих от распределения
    if parsed_arguments.distribution == "normal":
        # Q: может, для нормального распределения целых чисел их просто округлять или использовать биномиальное?
        if parsed_arguments.type != "float":
            raise ValueError("Normal distribution is only compatible with 'float' data type")
        if parsed_arguments.mean is None or parsed_arguments.std is None:
            raise ValueError("Normal distribution needs -mean and -std arguments")
        # Q: возможно, для нормального распределения оставить границы?
        if parsed_arguments.min_value is not None:
            raise ValueError("Normal distribution isn't compatible with -min_value argument")
        if parsed_arguments.max_value is not None:
            raise ValueError("Normal distribution isn't compatible with -max_value argument")

    if parsed_arguments.distribution == "uniform":
        param_list = [x for x in (parsed_arguments.mean, parsed_arguments.std, parsed_arguments.min_value, parsed_arguments.max_value) if x is not None]
        if len(param_list) < 2:
            raise ValueError("Not enought arguments for uniform distribution. Need either -min_value and -max_value or -mean and -std")
        elif len(param_list) > 2:
            raise ValueError("Too many arguments for uniform distribution. Need either -min_value and -max_value or -mean and -std")
        elif not(parsed_arguments.min_value is not None and parsed_arguments.max_value is not None or
                parsed_arguments.mean is not None and parsed_arguments.std is not None):
            raise ValueError("Invalid arguments. Need either -min_value and -max_value or -mean and -std")
        if parsed_arguments.min_value is not None and parsed_arguments.max_value is not None and parsed_arguments.min_value>parsed_arguments.max_value:
            raise ValueError("min_value cannot be greater than max_value")
