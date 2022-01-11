import sys


if __name__ == "__main__":

    # 读取第一行的n
    n = sys.stdin.readline().strip()
    words = n.split(',')

    # print(words)

    dic = {}
    results = str()
    
    for i in range(len(words)):

        if words[i] not in dic:
            dic[words[i]] = 1
        else:
            dic[words[i]] += 1

            if dic[words[i]] == 2:
                results += ('%s '%(words[i]))

    print(results.strip())