li $a0 6
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 4
sw $a0 0($sp)
addiu $sp $sp -4
jal sum_entry
sum_entry:
move $fp $sp
addiu $sp $sp -4
lw $a0 4($fp)
sw $a0 0($sp)
addiu $sp $sp -4
lw $a0 8($fp)
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
lw $ra 4($sp)
addiu $sp $sp 16
lw $fp 0($sp)
jr $ra
