# encoding: utf-8
from typing import List, Dict
from math import sqrt
import numpy.random as npr
import argparse

def number_list_to_str(number_list: List) -> str:
    res = ""
    for i in number_list:
        res += str(i)+'\n'
    return res

def generate_data(params: argparse.Namespace) -> str:
    npr.seed(params.seed)

    if params.distribution == "uniform" and params.min_value is None or params.max_value is None:
        # находим границы, если заданы матожидание и стандартное отклонение
        # для равномерного распределения std = b-a/sqrt(12)
        diff = params.std * sqrt(12)
        params.min_value = params.mean - diff/2
        params.max_value = params.mean + diff/2

    if params.type == "str":
        return generate_string_data(params)
    else:
        if params.type == "int":
            data = generate_integer_data(params)
        elif params.type == "float":
            data = generate_float_data(params)
        else:
            raise ValueError("unknown data type " + params.type + " in function generate_data")
        return number_list_to_str(data)

def generate_integer_data(params: argparse.Namespace):
    if params.distribution == "uniform":
        return npr.random_integers(params.min_value, params.max_value, params.data_len)
    else:
        raise ValueError("unknown distribution type " + params.distribution + " in function generate_integer_data")

def generate_float_data(params: argparse.Namespace):
    if params.distribution == "uniform":
        return npr.uniform(params.min_value, params.max_value, params.data_len)
    elif params.distribution == "normal":
        return npr.normal(params.mean, params.std, params.data_len)
    else:
        raise ValueError("unknown distribution type " + params.distribution + " in function generate_float_data")

def generate_string_data(params: argparse.Namespace):
    return npr.choice(params.charset, params.data_len)
