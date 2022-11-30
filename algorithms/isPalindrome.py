# 给你一个整数 x ，如果 x 是一个回文整数，返回 true ；否则，返回 false 。
# 回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。例如，121 是回文，而 123 不是。


class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """

        # 判断正负
        if x < 0:
            return False
        elif x > 0:
            
            xstr= str(abs(x))
            y = int(xstr[::-1])
            
            if x == y:
                return True
            else:
                return False
        else:
            return True


if __name__ == "__main__":
    test = Solution()
    print(test.isPalindrome(x=123))
    print(test.isPalindrome(x=-123))
    print(test.isPalindrome(x=121))