import time

picture_time = []
picture_time = time.strftime("%d", time.localtime(time.time()))
one = picture_time[0]
two = picture_time[1]
def num_to_string(num):
    numbers = {
      0: "t",
      1: "p",
      2: "s",
      3: "p",
    }
    return numbers.get(int(one))
def num_to_string2(num):
    numbers = {
      1: "a",
      2: "b",
      3: "c",
      4: "d",
      5: "e",
      6: "f",
      7: "g",
      8: "h",
      9: "y",
      0: "z",
    }
    return numbers.get(int(two))
def ver_code():
    verification_code = one + two + num_to_string(one)+num_to_string2(two)
    return verification_code