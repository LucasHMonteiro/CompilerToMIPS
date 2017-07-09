
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

    def f_call(self, p):
        string_builder = ""
        for i in p[::-1]:
            arg = str(self.integer(p[int(i)]))
            string_builder+='\n'+arg
            string_builder+='\nsw $a0 0($sp)'
            string_builder+= '\naddiu $sp $sp -4'
        return 'sw $fp 0($sp)' +\
               '\naddiu $sp $sp -4' +\
               string_builder +\
               '\njal f_entry'
