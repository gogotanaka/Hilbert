from h_lexer import *
import re
from sympy import Symbol, diff

precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
    )

vars = {}
funcs = {}

def lookupVars(var):
    try:
        return vars[var]
    except LookupError:
        return Symbol(var)

def p_statement_assign(p):
    'statement : VAR "=" expression'
    vars[p[1]] = p[3]

def p_statement_def_func(p):
    'statement : "f" FUNC_VARS "=" expression'
    funcs['f'] = { 'expr': p[4], 'vars': re.split(r', *', p[2].replace("(", "").replace(")", "")) }

def p_expression_diff_func(p):
    'expression : DIFF_SYM "(" expression ")"'
    p[0] = diff(p[3], Symbol(p[1].replace('d/d', '')))

def p_statement_eval_func(p):
    'expression : "f" FUNC_SUBS'
    expr = funcs['f']['expr']
    vs = funcs['f']['vars']
    p[0] = expr.subs([(Symbol(v), n) for v, n in zip(vs, p[2].replace("(", "").replace(")", ""))])

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_var(p):
    "expression : VAR"
    p[0] = lookupVars(p[1])

def p_expression_var_multi(p):
    "expression : VAR_MULTI"
    result = 1
    for c in p[1]: result *= lookupVars(c)
    p[0] = result

# def p_expression_eval_py(p):
#     'expression : EVAL_PY'
#     print(p[1])
#     exec(re.sub(r'py:', '', p[1]))

# def p_statement_def_func(p):
#     'statement : DEF_FUNC'
#     a = "def %s" % re.sub(r' *= *', ': return ', p[1])
#     print(a)
#     exec(a)
#
# def p_expression_eval_func(p):
#     'expression : EVAL_FUNC'
#     print("Syntax error at")
#     eval(1)

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()
parser = yacc