import sys


class Solution(object):

    def output(self,s):
        
        s = s.replace('\n', '')
        length = len(s)

        if length == 1:
            return [s]
            
        results = []
        for i in range(length):

            result = s[:i]+s[i+1:]
                
            temp = self.output(result)
                
            for j in temp:
                results.append(s[i:i+1]+j)
                
        return results


if __name__=='__main__':

    s = sys.stdin.readline()

    test = Solution()
    sys.stdout.write(str(test.output(s)))