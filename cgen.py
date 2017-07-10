
class CGen:

    def __init__():
        pass

    def integer(self, p):
        return '\nli $a0 %s' % (p[1])

    def add(self, p):
        return self.integer(p[1]) +\
               '\nsw $a0 0($sp)' +\
               '\naddiu $sp $sp -4' +\
                self.integer(p[3]) +\
                '\nlw $t1 4($sp)' +\
                '\nadd $a0 $t1 $a0' +\
                '\naddiu $sp $sp 4'

    def f_call(self, p):
        string_builder = ""
        for i in p[::-1]:
            arg = str(self.integer(p[i]))
            string_builder+='\n'+arg
            string_builder+='\nsw $a0 0($sp)'
            string_builder+= '\naddiu $sp $sp -4'
        return 'sw $fp 0($sp)' +\
               '\naddiu $sp $sp -4' +\
               string_builder +\
               '\njal f_entry'

    def f_def(self, p, number_params):
        return 'f_entry:' +\
           '\nmove $fp $sp' +\
           '\nsw $ra 0($sp)' +\
           '\naddiu $sp $sp -4' +\
           str(p[1]) +\
           '\nlw $ra 4($sp)' +\
           '\naddiu $sp $sp ' + str(4*number_params+8) +\
           '\nlw $fp 0($sp)' +\
           '\njr $ra'
