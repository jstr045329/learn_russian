import time

def now(shiftFromGMT=4*3600):
    return int(time.time() - shiftFromGMT)

if __name__ == "__main__":
    print(now())
