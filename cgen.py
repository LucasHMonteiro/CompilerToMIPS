
class CGen:

    def __init__(self, tree, symbol_table):
        self.file = open('teste.asm', 'w')
        self.tree = tree
        self.vars = []
        self.functions = symbol_table
        self.curr_func = ''
    
    def gen(self):
        for i in range(len(self.tree)):
            if self.tree[i][0] == 'CGEN_ASSIGN':
                self.file.write('li $a0 %s\n' % (self.tree[i][2]))
                self.file.write('sw $a0 0($sp)\n')
                self.file.write('addiu $sp $sp -4\n')
                if self.tree[i+1][0] != 'CGEN_ASSIGN':
                    self.file.write('jal '+self.tree[i+1][1]+'_entry\n')
            else:
                self.functions[self.tree[i][1]] = self.tree[i][2]
                self.vars = list(reversed(self.functions[self.tree[i][1]]))
                self.curr_func = self.tree[i][1]
                self.func_def(self.tree[i])
        self.file.close()
    
    def func_def(self, inst):
        self.file.write(inst[1]+'_entry:\n')
        self.file.write('move $fp $sp\n')
        self.file.write('addiu $sp $sp -4\n')
        self.exp(inst[3])
        self.file.write('lw $ra 4($sp)\n')
        self.file.write('addiu $sp $sp %s\n' % (4*len(inst[2]) + 8))
        self.file.write('lw $fp 0($sp)\n')
        self.file.write('jr $ra\n')
    
    def exp(self, inst):
        if type(inst) == tuple:
            if inst[0] == 'CGEN_CALL':
                self.call(inst)
            elif inst[0] == 'CGEN_IF':
                self.if_stat(inst)
            elif inst[0] == 'CGEN_SUM':
                self._sum(inst)
            elif inst[0] == 'CGEN_SUB':
                self.sub(inst)
            elif inst[0] == 'CGEN_MULT':
                self.mult(inst)
            elif inst[0] == 'CGEN_DIV':
                self.div(inst)
        elif type(inst) == str:
            self.ident(inst)
        else:
            self.integer(inst)

    def call(self, inst):
        self.vars = list(reversed(self.functions[self.curr_func]))
        self.file.write('sw $fp 0($sp)\n')
        self.file.write('addiu $sp $sp -4\n')
        for arg in inst[2]:
            self.exp(arg)
            self.file.write('sw $a0 0($sp)\n')
            self.file.write('addiu $sp $sp -4\n')
        self.file.write('jal %s_entry\n' % inst[1])

    def ident(self, inst):
        self.file.write('lw $a0 %s($fp)\n' % (4*(self.vars.index(inst)+1)))

    def integer(self, inst):
        self.file.write('li $a0 %s\n' % inst)

    def _sum(self, inst):
        self.exp(inst[1])
        self.file.write('sw $a0 0($sp)\n')
        self.file.write('addiu $sp $sp -4\n')
        self.exp(inst[2])
        self.file.write('lw $t1 4($sp)\n')
        self.file.write('add $a0 $t1 $a0\n')
        self.file.write('addiu $sp $sp 4\n')

    def sub(self, inst):
        self.exp(inst[1])
        self.file.write('sw $a0 0($sp)\n')
        self.file.write('addiu $sp $sp -4\n')
        self.exp(inst[2])
        self.file.write('lw $t1 4($sp)\n')
        self.file.write('sub $a0 $a0 $t1\n')
        self.file.write('addiu $sp $sp 4\n')

    def mult(self, inst):
        self.exp(inst[1])
        self.file.write('sw $a0 0($sp)\n')
        self.file.write('addiu $sp $sp -4\n')
        self.exp(inst[2])
        self.file.write('lw $t1 4($sp)\n')
        self.file.write('mult $t1 $a0\n')
        self.file.write('mflo $a0\n')
        self.file.write('addiu $sp $sp 4\n')

    def div(self, inst):
        self.exp(inst[1])
        self.file.write('sw $a0 0($sp)\n')
        self.file.write('addiu $sp $sp -4\n')
        self.exp(inst[2])
        self.file.write('lw $t1 4($sp)\n')
        self.file.write('div $a0 $t1\n')
        self.file.write('mflo $a0\n')        
        self.file.write('addiu $sp $sp 4\n')

    def if_stat(self, inst):
        if(inst[2] == '=='):
            self.exp(inst[1])
            self.file.write('sw $a0 0($sp)\n')
            self.file.write('addiu $sp $sp -4\n')
            self.exp(inst[3])
            self.file.write('lw $t1 4($sp)\n')
            self.file.write('addiu $sp $sp 4\n')
            self.file.write('beq $a0 $t1 true_branch\n')
            self.file.write('false_branch:\n')
            self.exp(inst[5])
            self.file.write('b end_if\n')
            self.file.write('true_branch:\n')
            self.exp(inst[4])
            self.file.write('end_if:\n')