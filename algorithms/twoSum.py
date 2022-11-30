class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """

        for idx,val in enumerate(nums):

            # 循环搜索
            if target-val in nums:
                
                # 判断搜索到的是不是自己
                idy = nums.index(target-val)
                if idy == idx:
                    continue
                else:
                    return [idx,idy]

    
if __name__ == "__main__":
    test = Solution()
    print(test.twoSum(nums=[2,7,11,15],target=9))
    print(test.twoSum(nums=[3,2,4],target=6))