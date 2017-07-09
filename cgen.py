
class CGen:

    def __init__():
        pass

    def integer(self, p):
        return 'li $a0 %s' % (p[1])

    def paren(self, p):
        return self.e(p[2])

    def factor(self, p):
        return self.paren(p[1])

    def term(self, p):
        op = ''
        if p[2] == '*':
            op = 'mult'
        else:
            op = 'div'
        return self.integer(p[1]) +\
               '\nsw $a0 0($sp)' +\
               '\naddiu $sp $sp - 4' +\
                self.factor(p[3]) +\
                '\nlw $t1 4($sp)' +\
                '\n'+op+' $a0 $t1 $a0' +\
                '\naddiu $sp $sp 4'

    def arit(self, p):
        op = ''
        if p[2] == '+':
            op = 'add'
        else:
            op = 'sub'
        return self.integer(p[1]) +\
               '\nsw $a0 0($sp)' +\
               '\naddiu $sp $sp - 4' +\
                self.term(p[3]) +\
                '\nlw $t1 4($sp)' +\
                '\n'+op+' $a0 $t1 $a0' +\
                '\naddiu $sp $sp 4'

    