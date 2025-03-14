import re


def split_segments(text):
    pattern = r'\[开始-(\d+)\](.*?)\[结束-\1\]'
    _ = [match[1].strip() for match in re.findall(pattern, text, re.DOTALL)]
    ret = []
    for i in _:
        l = []
        for j in range(len(i.split("\n"))):
            l.append(i.split("\n")[j])
        ret.append(l)
    # print(ret)
    return ret, _


if __name__ == "__main__":
    with open("test.txt", 'r') as f:
        _, ret = split_segments(f.read())

        for i in ret:
            for j in range(len(i.split("\n"))):
                print("[" + str(j) + "] ", end="")
                print(i.split("\n")[j])
            print("")
