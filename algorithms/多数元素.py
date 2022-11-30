# ==================================
# 
# 多数元素
# 给定一个大小为 n 的数组，找到其中的多数元素。多数元素是指在数组中出现次数 大于 ⌊ n/2 ⌋ 的元素。
# 你可以假设数组是非空的，并且给定的数组总是存在多数元素。
# 示例1：
#   输入：[3,2,3]
#   输出：3
# 示例2：
#   输入：[2,2,1,1,1,2,2]
#   输出：2
# 
# ==================================


from typing import List
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        
        count = 0
        candidate = None

        for num in nums:
            if count == 0:
                candidate = num
            count += (1 if num == candidate else -1)

        return candidate

if __name__ == "__main__":
    test = Solution()
    print(test.majorityElement([3,2,3]))
    print(test.majorityElement([2,2,1,1,1,2,2]))