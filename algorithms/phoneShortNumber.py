class Solution(object):
    def phoneShort(self, phone):
        
        phone = str(phone)

        # 判断是不是11位
        if len(phone) == 11:

            last5 = phone[6:12]
            phoneShort = '6' + last5

        return phoneShort


if __name__ == "__main__":
    test = Solution()
    print(test.phoneShort(18233396543))
        