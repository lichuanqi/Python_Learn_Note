class Solution(object):

    def maxDistToClosest(self, seats):
        """
        :type seats: List[int]
        :rtype: int
        """

        nums = len(seats)

        seats_diff = []
        diff_same = []
        max_diff = 0

        for i in range(0,nums-1):

            diff = seats[i+1] - seats[i]
            seats_diff.append(diff)

            if diff == 0:
                max_diff += 1
                diff_same.append(max_diff)
            else:
                diff_same.append(max_diff)
                max_diff = 0

        print(seats_diff)
        print(diff_same)

        return max(diff_same)

    

if __name__ == "__main__":
    test = Solution()
    print(test.maxDistToClosest([1,0,0,0]))