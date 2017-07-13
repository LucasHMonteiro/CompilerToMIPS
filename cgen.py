
class CGen:

    def integer(self, p):
        if p:
            return 'li $a0 %s' % (p[1])

    def name(self, i):
        return 'lw $a0 %d($fp)' % (i*4)

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
        return self.term(p[1]) +\
               '\nsw $a0 0($sp)' +\
               '\naddiu $sp $sp - 4' +\
                self.factor(p[3]) +\
                '\nlw $t1 4($sp)' +\
                '\n'+op+' $a0 $t1 $a0' +\
                '\naddiu $sp $sp 4'

    def arit(self, p):
        print(p.__dict__)
        op = ''
        if p[2] == '+':
            op = 'add'
        else:
            op = 'sub'
        return self.arit(p[1]) +\
               '\nsw $a0 0($sp)' +\
               '\naddiu $sp $sp - 4' +\
               self.term(p[3]) +\
               '\nlw $t1 4($sp)' +\
               '\n'+op+' $a0 $t1 $a0' +\
               '\naddiu $sp $sp 4'

    def if_stat(self, p):
        return self.e(p[2]) +\
               'sw $a0 0($sp)' +\
               'addiu $sp $sp -4' +\
               self.e(p[4]) +\
               'lw $t1 4($sp)' +\
               'addiu $sp $sp 4' +\
               'beq $a0 $t1 true_branch' +\
               'false_branch:' +\
               self.e(p[6]) +\
               'b end_if' +\
               'true_branch:' +\
               self.e(p[8]) +\
               'end_if:'

    def f_call(self, p):
        output = 'sw $fp 0($sp)' +\
                 'addiu $sp $sp -4'
        for param in p[3]:
            output += self.e(param) +\
                      'sw $a0 0($sp)' +\
                      'addiu $sp $sp -4'
        output += 'jal '+p[1]+'_entry'
        return output

    def e(self, p, args_hash=None):
        # print(p.__dict__)
        if p.slice[1].type == 'INTEGER':
            return self.integer(p)
        elif p.slice[1].type == 'ID' and len(p) == 5:
            return self.f_call(p)
        elif p.slice[1].type == 'IF':
            return self.if_stat(p)
        elif p.slice[1].type == 'ID' and args_hash:
            self.name(len(args_hash)-args_hash[p[1]])
