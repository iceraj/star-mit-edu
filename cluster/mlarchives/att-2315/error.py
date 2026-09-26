__author__ = 'yxue'

def imp(fname):
    if fname[-3:] == '.py':
        fname = fname[:-3]
    exec('import ' + fname + ' as params')
    print params.alpha
    f = open(fname+'_alpha.txt', 'w')
    f.write('%f' % params.alpha)
    f.close()



