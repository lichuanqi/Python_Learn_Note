# ================================
#
# 找出字符数最多的单词
#
# ================================


class Solution:

    def longestList(self, sens):
        
        word = ''
        wordlen = 0

        words = sens.split(' ')

        for i in range(len(words)):

            if len(words[i]) > wordlen:
                word = words[i]
                wordlen = len(words[i])
            else:
                continue

        print('%s:%s'%(word,wordlen))


if __name__ == "__main__":
    test = Solution()
    print(test.longestList('I Love China'))