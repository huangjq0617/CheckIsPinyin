# -*- coding: utf-8 -*-

"""

Created on 2018/10/18 上午11:15

@author: jqhuang

"""

import os


class CheckStringIsPinyin(object):

    def __init__(self, pinyin_list_path='./pinyin_list.txt'):

        self.first_alpha_index_map = self.build_first_alpha_index_map(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), pinyin_list_path)
        )

    @staticmethod
    def build_first_alpha_index_map(pinyin_list_path):

        index_map = {}

        print os.getcwd()
        if not os.path.exists(pinyin_list_path):
            return index_map

        with open(pinyin_list_path) as fp:

            lines = fp.readlines()
            for pinyin in lines:
                pinyin = pinyin.strip()
                pinyin_len = len(pinyin)

                if pinyin_len == 0:
                    pass

                first_alpha = pinyin[0]
                if first_alpha in index_map:
                    maxlen_pinyin_list = index_map[first_alpha]
                    maxlen_pinyin_list[1].add(pinyin)
                    if pinyin_len > maxlen_pinyin_list[0]:
                        maxlen_pinyin_list[0] = pinyin_len
                else:
                    pinyin_set = set()
                    pinyin_set.add(pinyin)
                    index_map[first_alpha] = [pinyin_len, pinyin_set]

        return index_map

    def check_string_is_pinyin(self, line):

        if isinstance(line, unicode):
            line = line.encode('utf-8')

        if len(line) == 0:
            return False

        to_check_list = [line]

        while len(to_check_list) > 0:

            s = to_check_list.pop(0)
            first_alpha = s[0]
            if first_alpha not in self.first_alpha_index_map:
                return False

            maxlen, possible_set = self.first_alpha_index_map[first_alpha]
            for i in range(min(len(s), maxlen), 0, -1):
                cheched = s[:i]
                remained = s[i:]
                if cheched in possible_set:
                    if len(remained) == 0:
                        return True
                    else:
                        to_check_list.append(remained)

        return False

    def get_all_pinyin_tokens(self, line):

        if isinstance(line, unicode):
            line = line.encode('utf-8')

        all_hyp_result = []

        if len(line) == 0:
            return all_hyp_result

        to_check_list = [(line, '', -1)]
        index = 0

        checked_add_remain_cache = set()

        while index < len(to_check_list):

            s = to_check_list[index][0]
            first_alpha = s[0]
            if first_alpha not in self.first_alpha_index_map:
                return all_hyp_result

            maxlen, possible_set = self.first_alpha_index_map[first_alpha]
            for i in range(min(len(s), maxlen), 0, -1):
                checked = s[:i]
                remained = s[i:]

                if checked in possible_set:
                    if len(remained) == 0:
                        tokened_pinyin = [checked]
                        prefix_index = index
                        while True:
                            _, prefix_checked, prefix_index = to_check_list[prefix_index]
                            tokened_pinyin.append(prefix_checked)
                            if prefix_index <= 0:
                                break

                        # return True, ' '.join(tokened_pinyin[::-1])
                        all_hyp_result.append(' '.join(tokened_pinyin[::-1]))
                        break

                    else:
                        tmp = remained + '+' + checked
                        if tmp not in checked_add_remain_cache:
                            to_check_list.append((remained, checked, index))
                            checked_add_remain_cache.add(tmp)

            index += 1

        return all_hyp_result


if __name__ == '__main__':

    checkIsPinyin = CheckStringIsPinyin()

    print checkIsPinyin.check_string_is_pinyin('abc')

    print checkIsPinyin.get_all_pinyin_tokens('guangangei')
    print checkIsPinyin.get_all_pinyin_tokens('alone')

