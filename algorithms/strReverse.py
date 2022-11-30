class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        # 判断范围
        if abs(x) > 2**31:
            return 0

        # 判断正负
        if x < 0:
            danwei  = -1
        elif x > 0:
            danwei = 1
        else:
            danwei = 0

        xstr= str(abs(x))

        return danwei * int(xstr[::-1])


if __name__ == "__main__":
    test = Solution()
    print(test.reverse(x=123))
    print(test.reverse(x=-123))
    print(test.reverse(x=120))
    print(test.reverse(x=1534236469))
    print(test.reverse(x=15342364690))