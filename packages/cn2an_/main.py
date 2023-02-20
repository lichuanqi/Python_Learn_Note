"""
cn2an 是一个快速转化 中文数字 和 阿拉伯数字 的工具包！
https://github.com/Ailln/cn2an
"""
import cn2an


# =========== 中文数字 => 阿拉伯数字 ===========
# 在 strict 模式（默认）下，只有严格符合数字拼写的才可以进行转化
output = cn2an.cn2an("一百二十三", "strict")
print(output)

# 在 normal 模式下，可以将 一二三 进行转化
output = cn2an.cn2an("一二三", "normal")
print(output)

# 在 smart 模式下，可以将混合拼写的 1百23 进行转化
output = cn2an.cn2an("1百23", "smart")
print(output)

# 以上三种模式均支持负数
output = cn2an.cn2an("负一百二十三", "strict")
print(output)

# 以上三种模式均支持小数
output = cn2an.cn2an("一点二三", "strict")
print(output)


# =========== 阿拉伯数字 => 中文数字 ===========
# 在 low 模式（默认）下，数字转化为小写的中文数字
output = cn2an.an2cn("123")
# 或者
output = cn2an.an2cn("123", "low")
# output:
# 一百二十三

# 在 up 模式下，数字转化为大写的中文数字
output = cn2an.an2cn("123", "up")
# output:
# 壹佰贰拾叁

# 在 rmb 模式下，数字转化为人民币专用的描述
output = cn2an.an2cn("123", "rmb")
# output:
# 壹佰贰拾叁元整

# 以上三种模式均支持负数
output = cn2an.an2cn("-123", "low")
# output:
# 负一百二十三

# 以上三种模式均支持小数
output = cn2an.an2cn("1.23", "low")
# output:
# 一点二三


# =========== 句子转化: 中文数字 => 阿拉伯数字 ===========
# 在 cn2an 方法（默认）下，可以将句子中的中文数字转成阿拉伯数字
output = cn2an.transform("小王捡了一百块钱")
# 或者
output = cn2an.transform("小王捡了一百块钱", "cn2an")
# output:
# 小王捡了100块钱

## 支持日期
output = cn2an.transform("小王的生日是二零零一年三月四日", "cn2an")
# output:
# 小王的生日是2001年3月4日

## 支持分数
output = cn2an.transform("抛出去的硬币为正面的概率是二分之一", "cn2an")
# output:
# 抛出去的硬币为正面的概率是1/2

## 支持百分比
## 支持摄氏度

# =========== 句子转化: 阿拉伯数字 => 中文数字 ===========
# 在 an2cn 方法下，可以将句子中的中文数字转成阿拉伯数字
output = cn2an.transform("道段:13路, 34563部队", "an2cn")
print(output)

# 日期
output = cn2an.transform("小王的生日是2001年3月4日", "an2cn")
print(output)
# output:
# 小王的生日是二零零一年三月四日

# 分数
output = cn2an.transform("抛出去的硬币为正面的概率是1/2", "an2cn")
print(output)
# output:
# 抛出去的硬币为正面的概率是二分之一