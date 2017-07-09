
class CGen:

    def __init__():
        pass

    def integer(self, p):
        return 'li $a0 %s' % (p[1])

    def add(self, p):
        return self.integer(p[1]) +\
               '\nsw $a0 0($sp)' +\
               'addiu $sp $sp - 4' +\
                self.integer(p[3]) +\
                'lw $t1 4($sp)' +\
                'add $a0 $t1 $a0' +\
                'addiu $sp $sp 4'