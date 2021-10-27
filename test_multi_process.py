'''
    Can't run on MACOS.
'''
PARALLELPROCESSDATA = None


def launchParallelProcess(val):
    global PARALLELPROCESSDATA

    PARALLELPROCESSDATA = val

    from multiprocessing import Process
    p = Process(target=_launchParallelProcess, args=tuple([]))
    p.start()
    return p


def _launchParallelProcess():
    global PARALLELPROCESSDATA
    val = PARALLELPROCESSDATA
    print('val:', val)


if __name__ == '__main__':
    launchParallelProcess(1)
    print(PARALLELPROCESSDATA)
