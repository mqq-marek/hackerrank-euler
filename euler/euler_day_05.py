"""
Euler challenge from HackerRank https://www.hackerrank.com/contests/projecteuler/challenges/euler254/problem

Speed, speed, ... improvement - Day 4

"""

import cProfile, pstats, io
import contextlib
import math
import time
from collections import defaultdict, namedtuple
from functools import reduce
from itertools import combinations

DEBUG = False
F9 = 362880
sg_cache = {}
sg_mod_cache = {}
PREFIX = {}
FACTORIALS = [math.factorial(i) for i in range(10)]
PREF_I = [
    (181, 295039, "134445555666778888888"),
    (182, 261119, "122333444455566666777888888"),
    (183, 227199, "123345557777788888"),
    (184, 193279, "1344455667777778888"),
    (185, 159359, "1223334444566667777777888"),
    (186, 125439, "123345666666888"),
    (187, 91519, "1344467788"),
    (188, 57599, "122333444455555667778"),
    (189, 23679, "123345555566667777"),
    (190, 47359, "1344455556678"),
    (191, 71039, "12233344445557777778"),
    (192, 94719, "12334555666667788"),
    (193, 118399, "1344455666777777788"),
    (194, 142079, "1223334444567777888"),
    (195, 165759, "1233456666668888"),
    (196, 189439, "134446666777778888"),
    (197, 213119, "12233344445555567788888"),
    (198, 236799, "123345555566666677777788888"),
    (199, 110719, "1344455556666667777788"),
    (200, 347519, "1223334444555666666777788888888"),
    (201, 221439, "1233455566666677788888"),
    (202, 95359, "13444556666667788"),
    (203, 332159, "12233344445666666788888888"),
    (204, 206079, "12334566666688888"),
    (205, 79999, "1344466666677777778"),
    (206, 316799, "122333444455555666667777778888888"),
    (207, 190719, "123345555566666777778888"),
    (208, 18559, "1344455556666777"),
    (209, 209279, "1223334444555666788888"),
    (210, 37119, "12334555667777777"),
    (211, 227839, "134445567777788888"),
    (212, 55679, "122333444457778"),
    (213, 246399, "123345666666888888"),
    (214, 74239, "13444666667777778"),
    (215, 264959, "1223334444555556667777888888"),
    (216, 92799, "1233455555667788"),
    (217, 185599, "1344455556666677778888"),
    (218, 278399, "122333444455567777777888888"),
    (219, 8319, "1233455566667"),
    (220, 101119, "1344455777788"),
    (221, 193919, "122333444456667777778888"),
    (222, 286719, "1233456666668888888"),
    (223, 16639, "1344466777"),
    (224, 109439, "12233344445555566667777788"),
    (225, 202239, "123345555588888"),
    (226, 41599, "13444555568"),
    (227, 243839, "122333444455566888888"),
    (228, 83199, "1233455566688"),
    (229, 285439, "134445566668888888"),
    (230, 124799, "1223334444566666888"),
    (231, 327039, "12334566666688888888"),
    (232, 166399, "1344478888"),
    (233, 5759, "1223334444555557"),
    (234, 207999, "12334555556788888"),
    (235, 53119, "134445555666778"),
    (236, 261119, "122333444455566666777888888"),
    (237, 106239, "123345557777788"),
    (238, 314239, "1344455667777778888888"),
    (239, 159359, "1223334444566667777777888"),
    (240, 4479, "123345666666"),
    (241, 212479, "1344467788888"),
    (242, 57599, "122333444455555667778"),
    (243, 265599, "123345555566667777888888"),
    (244, 168319, "1344455556678888"),
    (245, 71039, "12233344445557777778"),
    (246, 336639, "12334555666667788888888"),
    (247, 239359, "1344455666777777788888"),
    (248, 142079, "1223334444567777888"),
    (249, 44799, "1233456666668"),
    (250, 310399, "134446666777778888888"),
    (251, 213119, "12233344445555567788888"),
    (252, 115839, "123345555566666677777788"),
    (253, 231679, "1344455556666667777788888"),
    (254, 347519, "1223334444555666666777788888888"),
    (255, 100479, "1233455566666677788"),
    (256, 216319, "13444556666667788888"),
    (257, 332159, "12233344445666666788888888"),
    (258, 85119, "12334566666688"),
    (259, 200959, "1344466666677777778888"),
    (260, 316799, "122333444455555666667777778888888"),
    (261, 69759, "123345555566666777778"),
    (262, 139519, "1344455556666777888"),
    (263, 209279, "1223334444555666788888"),
    (264, 279039, "12334555667777777888888"),
    (265, 348799, "134445567777788888888"),
    (266, 55679, "122333444457778"),
    (267, 125439, "123345666666888"),
    (268, 195199, "13444666667777778888"),
    (269, 264959, "1223334444555556667777888888"),
    (270, 334719, "1233455555667788888888"),
    (271, 306559, "1344455556666677778888888"),
    (272, 278399, "122333444455567777777888888"),
    (273, 250239, "1233455566667888888"),
    (274, 222079, "1344455777788888"),
    (275, 193919, "122333444456667777778888"),
    (276, 165759, "1233456666668888"),
    (277, 137599, "1344466777888"),
    (278, 109439, "12233344445555566667777788"),
    (279, 81279, "123345555588"),
    (280, 162559, "13444555568888"),
    (281, 243839, "122333444455566888888"),
    (282, 325119, "1233455566688888888"),
    (283, 43519, "134445566668"),
    (284, 124799, "1223334444566666888"),
    (285, 206079, "12334566666688888"),
    (286, 287359, "1344478888888"),
    (287, 5759, "1223334444555557"),
    (288, 87039, "12334555556788"),
    (289, 174079, "134445555666778888"),
    (290, 261119, "122333444455566666777888888"),
    (291, 348159, "123345557777788888888"),
    (292, 72319, "1344455667777778"),
    (293, 159359, "1223334444566667777777888"),
    (294, 246399, "123345666666888888"),
    (295, 333439, "1344467788888888"),
    (296, 57599, "122333444455555667778"),
    (297, 144639, "123345555566667777888"),
    (298, 289279, "1344455556678888888"),
    (299, 71039, "12233344445557777778"),
    (300, 215679, "12334555666667788888"),
    (301, 360319, "1344455666777777788888888"),
    (302, 142079, "1223334444567777888"),
    (303, 286719, "1233456666668888888"),
    (304, 68479, "134446666777778"),
    (305, 213119, "12233344445555567788888"),
    (306, 357759, "123345555566666677777788888888"),
    (307, 352639, "1344455556666667777788888888"),
    (308, 347519, "1223334444555666666777788888888"),
    (309, 342399, "1233455566666677788888888"),
    (310, 337279, "13444556666667788888888"),
    (311, 332159, "12233344445666666788888888"),
    (312, 327039, "12334566666688888888"),
    (313, 321919, "1344466666677777778888888"),
    (314, 316799, "122333444455555666667777778888888"),
    (315, 311679, "123345555566666777778888888"),
    (316, 260479, "1344455556666777888888"),
    (317, 209279, "1223334444555666788888"),
    (318, 158079, "12334555667777777888"),
    (319, 106879, "134445567777788"),
    (320, 55679, "122333444457778"),
    (321, 4479, "123345666666"),
    (322, 316159, "13444666667777778888888"),
    (323, 264959, "1223334444555556667777888888"),
    (324, 213759, "1233455555667788888"),
    (325, 64639, "1344455556666677778"),
    (326, 278399, "122333444455567777777888888"),
    (327, 129279, "1233455566667888"),
    (328, 343039, "1344455777788888888"),
    (329, 193919, "122333444456667777778888"),
    (330, 44799, "1233456666668"),
    (331, 258559, "1344466777888888"),
    (332, 109439, "12233344445555566667777788"),
    (333, 323199, "123345555588888888"),
    (334, 283519, "13444555568888888"),
    (335, 243839, "122333444455566888888"),
    (336, 204159, "1233455566688888"),
    (337, 164479, "134445566668888"),
    (338, 124799, "1223334444566666888"),
    (339, 85119, "12334566666688"),
    (340, 45439, "1344478"),
    (341, 5759, "1223334444555557"),
    (342, 328959, "12334555556788888888"),
]
PREF_START = PREF_I[0][0]
PREF_LEN = PREF_I[-1][0] - PREF_I[0][0] + 1
sg_table = [1, 2, 5, 6, 7, 3, 4, 5, 6, 7, 8, 8, 9, 13, 9, 10, 11, 13, 14, 15, 16, 17, 18, 13, 14, 15, 9, 10, 11, 12,
            13, 14, 12, 13, 14, 15, 19, 28, 24, 25, 37, 31, 32, 45, 46, 50, 66, 67, 71, 84, 89, 90, 114, 118, 134,
            154, 158, 193, 231, 235, 247, 317, 321, 545, 843, 1052, 1339, 1574, 1846, 2035, 2294, 2566, 5035, 7578,
            9997, 12529, 15009, 17415, 19912, 22416, 24933, 49686, 74498, 99334, 124135, 148899, 173672, 198536,
            223324, 248145, 496173, 744212, 992162, 1240190, 1488229, 1736179, 1984255, 2232318, 2480268, 4960419,
            7440581, 9920765, 12400916, 14881015, 17361186, 19841385, 22321571, 24801707, 49603317, 74404903,
            99206450, 124008025, 148809646, 173611193, 198412768, 223214413, 248015925, 496031816, 744047718,
            992063594, 1240079422, 1488095324, 1736111200, 1984127056, 2232142919, 2480158795, 4960317556,
            7440476328, 9920635039, 12400793737, 14880952509, 17361111207, 19841269933, 22321428666, 24801587412,
            49603174707, 74404761998, 99206349313, 124007936656, 148809523899, 173611111214, 198412698494,
            223214285824, 248015873187, 496031746194, 744047619212, 992063492204, 1240079365211, 1488095238229,
            1736111111221, 1984126984276, 2232142857318, 2480158730310, 4960317460440, 7440476190581, 9920634920744,
            12400793650874, 14880952381015, 17361111111165, 19841269841406, 22321428571571, 24801587301686,
            49603174603275, 74404761904903, 99206349206429, 124007936508046, 148809523809646, 173611111111172,
            198412698412789, 223214285714413, 248015873015967, 496031746031837, 744047619047718, 992063492063573,
            1240079365079443, 1488095238095324, 1736111111111179, 1984126984127014, 2232142857142919,
            2480158730158837, 4960317460317577, 7440476190476328, 9920634920635018, 12400793650793758,
            14880952380952509, 17361111111111186, 19841269841269891, 22321428571428666, 24801587301587391,
            49603174603174665, 74404761904761998, 99206349206349292, 124007936507936614, 148809523809523899,
            173611111111111193, 198412698412698515, 223214285714285824, 248015873015873166, 496031746031746152,
            744047619047619212]
PREFIX = {221439: '1233455566666677788888', 71679: '1233455567777778', 95359: '13444556666667788', 308479: '13444556777778888888', 332159: '12233344445666666788888888', 182399: '12233344445677778888', 206079: '12334566666688888', 56319: '12334567778', 79999: '1344466666677777778', 293119: '134446778888888', 316799: '122333444455555666667777778888888', 167039: '12233344445555578888', 190719: '123345555566666777778888', 144639: '123345555566667777888', 18559: '1344455556666777', 335359: '1344455556667788888888', 209279: '1223334444555666788888', 163199: '1223334444555668888', 37119: '12334555667777777', 353919: '12334555677777788888888', 227839: '134445567777788888', 181759: '134445577778888', 55679: '122333444457778', 9599: '122333444456666667', 246399: '123345666666888888', 200319: '1233456666677777778888', 74239: '13444666667777778', 28159: '13444666677777', 264959: '1223334444555556667777888888', 218879: '1223334444555556677788888', 92799: '1233455555667788', 357759: '123345555566666677777788888888', 185599: '1344455556666677778888', 87679: '13444555566788', 278399: '122333444455567777777888888', 180479: '1223334444555666667778888', 8319: '1233455566667', 273279: '123345556777777888888', 101119: '1344455777788', 3199: '13444556666', 193919: '122333444456667777778888', 95999: '1223334444577788', 286719: '1233456666668888888', 188799: '123345666777778888', 16639: '1344466777', 281599: '134446666667777777888888', 109439: '12233344445555566667777788', 11519: '122333444455555677', 202239: '123345555588888', 311679: '123345555566666777778888888', 41599: '13444555568', 151039: '13444555566666677777888', 243839: '122333444455566888888', 353279: '122333444455577777788888888', 83199: '1233455566688', 192639: '1233455567777778888', 285439: '134445566668888888', 31999: '134445566777777', 124799: '1223334444566666888', 234239: '1223334444566677777788888', 327039: '12334566666688888888', 73599: '12334566667777778', 166399: '1344478888', 275839: '1344466666777777888888', 5759: '1223334444555557', 115199: '1223334444555556666677777788', 207999: '12334555556788888', 213759: '1233455555667788888', 53119: '134445555666778', 58879: '13444555566667778', 261119: '122333444455566666777888888', 266879: '12233344445556666667777888888', 106239: '123345557777788', 111999: '12334555677777788', 314239: '1344455667777778888888', 319999: '134445566677777778888888', 159359: '1223334444566667777777888', 165119: '12233344445666668888', 4479: '123345666666', 10239: '12334577', 212479: '1344467788888', 218239: '134446677788888', 57599: '122333444455555667778', 63359: '12233344445555566677778', 265599: '123345555566667777888888', 323199: '123345555588888888', 168319: '1344455556678888', 225919: '13444555566666777788888', 71039: '12233344445557777778', 128639: '12233344445556667888', 336639: '12334555666667788888888', 31359: '123345556777777', 239359: '1344455666777777788888', 296959: '1344455666666778888888', 142079: '1223334444567777888', 199679: '12233344445666677777778888', 44799: '1233456666668', 102399: '12334566777788', 310399: '134446666777778888888', 5119: '134447', 213119: '12233344445555567788888', 270719: '122333444455555666677777888888', 115839: '123345555566666677777788', 328959: '12334555556788888888', 231679: '1344455556666667777788888', 81919: '134445555688', 347519: '1223334444555666666777788888888', 197759: '1223334444555677777778888', 100479: '1233455566666677788', 313599: '1233455567777778888888', 216319: '13444556666667788888', 66559: '13444556777778', 85119: '12334566666688', 298239: '12334567778888888', 200959: '1344466666677777778888', 51199: '134446778', 69759: '123345555566666777778', 23679: '123345555566667777', 139519: '1344455556666777888', 93439: '1344455556667788', 279039: '12334555667777777888888', 232959: '12334555677777788888', 348799: '134445567777788888888', 302719: '134445577778888888', 125439: '123345666666888', 79359: '1233456666677777778', 195199: '13444666667777778888', 149119: '13444666677777888', 334719: '1233455555667788888888', 236799: '123345555566666677777788888', 306559: '1344455556666677778888888', 208639: '13444555566788888', 250239: '1233455566667888888', 152319: '123345556777777888', 222079: '1344455777788888', 124159: '13444556666888', 165759: '1233456666668888', 67839: '123345666777778', 137599: '1344466777888', 39679: '134446666667777777', 81279: '123345555588', 162559: '13444555568888', 271999: '13444555566666677777888888', 325119: '1233455566688888888', 43519: '134445566668', 152959: '134445566777777888', 315519: '12334566667777778888888', 287359: '1344478888888', 33919: '1344466666777777', 87039: '12334555556788', 174079: '134445555666778888', 179839: '13444555566667778888', 348159: '123345557777788888888', 72319: '1344455667777778', 78079: '134445566677777778', 252159: '12334577888888', 333439: '1344467788888888', 339199: '134446677788888888', 289279: '1344455556678888888', 346879: '13444555566666777788888888', 215679: '12334555666667788888', 360319: '1344455666777777788888888', 55039: '1344455666666778', 344319: '12334566777788888888', 68479: '134446666777778', 126079: '134447888', 352639: '1344455556666667777788888888', 202879: '134445555688888', 342399: '1233455566666677788888888', 337279: '13444556666667788888888', 187519: '13444556777778888', 177279: '12334567778888', 321919: '1344466666677777778888888', 172159: '134446778888', 260479: '1344455556666777888888', 214399: '1344455556667788888', 158079: '12334555667777777888', 106879: '134445567777788', 60799: '134445577778', 321279: '1233456666677777778888888', 316159: '13444666667777778888888', 270079: '13444666677777888888', 64639: '1344455556666677778', 329599: '13444555566788888888', 129279: '1233455566667888', 343039: '1344455777788888888', 245119: '13444556666888888', 309759: '123345666777778888888', 258559: '1344466777888888', 160639: '134446666667777777888', 283519: '13444555568888888', 30079: '13444555566666677777', 204159: '1233455566688888', 164479: '134445566668888', 273919: '134445566777777888888', 194559: '12334566667777778888', 45439: '1344478', 154879: '1344466666777777888', 295039: '134445555666778888888', 300799: '13444555566667778888888', 227199: '123345557777788888', 193279: '1344455667777778888', 199039: '134445566677777778888', 131199: '12334577888', 91519: '1344467788', 97279: '134446677788', 47359: '1344455556678', 104959: '13444555566666777788', 94719: '12334555666667788', 118399: '1344455666777777788', 175999: '1344455666666778888', 223359: '12334566777788888', 189439: '134446666777778888', 247039: '134447888888', 110719: '1344455556666667777788', 323839: '134445555688888888'}
N_Number = namedtuple("N_Number", "prefix suffix_len")


def init_prefixes():
    assert_sg(True)


def digits_gen(n):
    """
    Yields number n digits in reverse sequence. For n = 342 sequence is 2, 4, 3
    :param n:
    :return:
    """
    while True:
        yield n % 10
        n //= 10
        if not n:
            break


def digits_sum(n):
    """ Return sum of digits n. """
    if isinstance(n, int):
        return sum([d for d in digits_gen(n)])
    elif isinstance(n, str):
        return sum([ord(d) - ord('0') for d in n])
    else:
        return sum([d for d in n.digits_gen()])


def f_value_with_digit_sum(n):
    """ Build the smallest number which digit sum is n. """
    n9, d = divmod(n, 9)
    if d == 0:
        return '9' * n9
    else:
        return chr(d+ord('0')) + '9' * n9


def reverse_f(f_value):
    """ Return number such that f(number) = f_value. """
    suffix_len, f_prefix = divmod(f_value, FACTORIALS[9])
    prefix = PREFIX[f_prefix]
    return N_Number(prefix, suffix_len)


def f(n):
    """
    Define f(n) as the sum of the factorials of the digits of n.
    For example:
        f(342) = 3! + 4! + 2! = 32
    :param n: number
    :return: sum digits factorial of n
    """
    if isinstance(n, str):
        n = int(n)
    if isinstance(n, int):
        return sum([FACTORIALS[d] for d in digits_gen(n)])
    elif isinstance(n, list):
        return sum([FACTORIALS[d] for d in n])
    else:
        return sum([FACTORIALS[d] for d in n.digits_gen()])


def sf(n):
    """
    Compute sf(n) as the sum of the digits of f(n).
    Store in sf_cache the value n for which the reached the first time key sf(n)
    So:
    sf(144) = 4 + 9 = 13 as f(144) is 1!+4!+4! = 49
    For n = 144 is minimum n such that sf(n) = 13 so sf_cache[13] = 144
    :param n: number
    :return: sum digits of f(n)
    """
    sf_ = digits_sum(f(n))
    return sf_


def g(i):
    """
    Define g(i) to be the smallest positive integer n such that sf(n) == i.
    sf(342) = 5, also sf(25) = 5 and 25 is the smallest number giving sf(i) = 5, so g(5) = 25
    Using cached value. g_sequence with parameter not less than i must be called earlier
    :param i: number
    :return: the smallest n such that sf(n) == i in as N_Number tuple
    """
    f_value = f_value_with_digit_sum(i)
    best_n = reverse_f(int(f_value))
    return best_n


def g_sequence(max_i):
    """
    Looks for g(i) in range 1..max_i
    Define g(i) to be the smallest positive integer n such that sf(n) == i.
    sf(342) = 5, also sf(25) = 5 and 25 is the smallest number giving sf(i) = 5, so g(5) = 25
    As n start be huge numbers - million and more digits we store in cache sg(n) which is digits sum of n
    Results are in a global cached dictionary
    :param max_i: range for compute g(i) from 1 to max_i
    :return: None
    """

    for i in range(1, max_i + 1):
        if sg_cache.get(i):
            continue
        f_value = f_value_with_digit_sum(i)
        best_n = reverse_f(int(f_value))
        if DEBUG:
            l_str = str(len(str(best_n.prefix)) + best_n.suffix_len)
            if len(l_str) > 19:
                l_str = '...'+l_str[-16:]
            prefix = best_n.prefix + '+'
            print(
                f'len={l_str:21}, f(n) = {f_value:40}, '
                f'g({i}) = {prefix}9*{best_n.suffix_len}')
        sg_cache[i] = digits_sum(best_n.prefix) + 9 * best_n.suffix_len
    return


def sg(i):
    """
    Define  sg(i) as the sum of the digits of g(i).
    So sg(5) = 2 + 5 = 7 as g(5) = 25.
    :param i:
    :return: sum digits of g(i)
    """
    if i <= len(sg_table):
        return sg_table[i-1]
    else:
        n = g(i)
        return digits_sum(n.prefix) + n.suffix_len * 9


def sum_sg_mod(n, m):

    def get_sg(i, m):
        nonlocal last_n, n9_step, step_r, last_sg9_sum, f_value_step, n9_rem
        f_value = f_value_with_digit_sum(i)
        n = reverse_f(int(f_value))
        i_ = (i - PREF_START) % PREF_LEN
        f_pref = PREF_I[i_][1]
        pref_ = PREF_I[i_][2]
        assert n.prefix == pref_
        print(f"F_ValPrefix: {f_value[0]}/{i%9}, Last_n: {last_n}, curr_n: {n.suffix_len}, inc: {n.suffix_len-last_n}")
        print(f"Prev Diff: {f_value_step}, step n/r: {n9_step}/{step_r}")
        if i % 9 == 1:
            inc, n9_rem = divmod(10 * n9_rem, F9)
            n9_step = 10 * n9_step + inc
            f_value_step = f_value_step * 10
        # step_n, step_r, cur_r are current step parameters
        if f_pref < step_r:
            carry = 1
        else:
            carry = 0
        n_inc = n9_step + carry
        step_r = f_pref

        assert n_inc + last_n == n.suffix_len
        last_n += n_inc
        last_sg9_sum = last_sg9_sum + n_inc
        sg_ = n.suffix_len * 9 + digits_sum(n.prefix)
        return sg_

    s = 0
    s = sum(sg_table[0:min(len(sg_table), n)]) % m

    f_value = f_value_with_digit_sum(len(sg_table))
    f_value_step = int(f_value[1:]) + 1
    nn = reverse_f(int(f_value))
    n9_step, n9_rem = divmod(f_value_step, F9)
    i_ = (len(sg_table) - PREF_START) % PREF_LEN
    step_r = PREF_I[i_][1]
    last_n = n.suffix_len
    last_sg9_sum = nn.suffix_len * 9

    for i in range(len(sg_table) + 1, n + 1):
        s = (s + get_sg(i, m)) % m
    return s


def sum_sg(n):
    s = 0
    s = sum(sg_table[0:min(len(sg_table), n)])

    for i in range(len(sg_table) + 1, n + 1):
        s = (s + sg(i))
    return s


def assert_sg(cache=None):

    for i, sg_sum in enumerate(sg_table, 1):
        if sg_cache.get(i):
            if sg_cache.get(i) != sg_sum:
                print(f'Assertion error sg({i}) is {sg_cache.get(i, 0)} while expected {sg_sum}')
        else:
            if cache:
                sg_cache[i] = sg_sum


def dic_as_list(dic, *, seq=True):
    lst = []
    for k in range(1, max(dic.keys())+1):
        if dic.get(k):
            lst.append(dic[k])
        elif seq:
            break
        else:
            lst.append(None)
    return lst


def make_sgi_mod_table(base_value=181):
    # init_prefixes()
    di = defaultdict(list)
    dv = defaultdict(set)
    dist = set()
    for i in range(base_value, 50001):
        f_v = int(f_value_with_digit_sum(i))
        n = reverse_f(f_v)
        d = f_v % FACTORIALS[9]
        dist.add(d)
        if n.suffix_len * 9 > 1000000000000:
            v = n.suffix_len * 9 % 1000000000000
            dv[d].add(v)
        di[d].append(i)
    distances = sorted(list(dist))

    dic = {}
    for d in distances:
        vl = list(dv[d])
        v = ""
        if len(vl) == 1:
            v = str(vl[0])
        else:
            v = vl
        dd = defaultdict(int)
        for i in range(1, len(di[d])):
            dd[di[d][i] - di[d][i - 1]] += 1
        s = ""
        if len(dd) == 1:
            s = list(dd.keys())[0]
        elif len(dd) == 2:
            dic[di[d][1]] = (d, di[d][3] - di[d][1])
            s = di[d][2] - di[d][0]
        else:
            s = dd
        dic[di[d][0]] = (d, s)
    min_pos = min(dic.keys())
    max_pos = max(dic.keys())
    for p in range(min_pos, max_pos):
        d, step = dic[p]
        if p + step < max_pos and not dic.get(p + step):
            dic[p + step] = (d, step)

    sgi_mod_table = []
    for p, (d, s) in sorted(dic.items()):
        sgi_mod_table.append((p, d, PREFIX[d], sf(PREFIX[d])))
    return sgi_mod_table


def show_prefix_list():
    with open("prefix.csv", "w") as file:
        with contextlib.redirect_stdout(file):
            print("prefix\tf(prefix)\tfs(prefix)\tlen(prefix)")
            for k, v in PREFIX.items():
                print(f'"{v}"\t{k}\t{digits_sum(k)}\t{len(str(v))}')


def show_suffix_list():
    with open("suffix.csv", "w") as file:
        with contextlib.redirect_stdout(file):
            print("suffix\tf(suffix)\tfs(suffix)\tlen(suffix)")
            for i in range(10001):
                print(f"'9'*{i}\t{i*FACTORIALS[9]}\t{digits_sum(i*FACTORIALS[9])}\t{i}")

def print_const_tables():
    # print(f'g_table = {dic_as_list(g_cache)}')
    # print(f'sg_table = {dic_as_list(sg_cache)}')
    #prefixes = [f(p) for p in dic_as_list(PREFIX)]
    #print(f'PREFIX = {prefixes}')
    hook_value = 181
    print(f'sgi_mod_table = {make_sgi_mod_table(hook_value)}')


def hacker_main():
    init_prefixes()
    assert_sg(cache=True)
    q = int(input())
    for _ in range(q):
        n, m = map(int, input().split())
        r = sum_sg_mod(n, m)
        print(r)


def profile_main(size=200):
    with cProfile.Profile() as pr:
        init_prefixes()
        sum_sg(size)

    s = io.StringIO()
    sort_by = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()
    print(s.getvalue())


def development_main(size=200, mod=None):
    pgm_start = time.perf_counter()
    init_prefixes()
    print(FACTORIALS)
    pgm_stop = time.perf_counter()
    print(f"Init prefixes - {pgm_stop - pgm_start:.2f} seconds")
    if mod:
        total = sum_sg_mod(size, mod)
    else:
        total = sum_sg(size)
    pgm_stop = time.perf_counter()
    print(f"sum_sg({size}) has length {len(str(total))} last digits are {total % 1000000000000000} "
          f"computed in {pgm_stop - pgm_start:.2f} seconds")
    assert_sg()
    print_const_tables()


if __name__ == "__main__":
    DEBUG = True
    # hacker_main()
    # profile_main(20000)
    development_main(250, True)
    exit()

"""
sum_sg(500) has length 52 last digits are 698412698459839 computed in 0.02 seconds

sum_sg(50000) has length 9 last digits are 132135059computed in 4.50 seconds
sum_sg(50000) has length 5552 last digits are 126984132135059 computed in 4.15 seconds



"""

