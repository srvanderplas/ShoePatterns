def generateColor(rand=True, print=False):
    '''
    Randomly generating a color hexcode'''
    import random
    r = lambda: random.randint(0,255)
    code = '#%02X%02X%02X' % (r(),r(),r())
    if print==True:
        print(code)
    return code
