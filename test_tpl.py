import unittest

from tpl import tpl_parse, tpl_eval

class TestParser(unittest.TestCase):
    def test_general(self):
        self.assertEqual(tpl_parse('(a b (+ 1 2))'), ['a', 'b', ['+', ['val', 1], ['val', 2]]])

    def test_parse_atom(self):
        self.assertEqual(tpl_parse('foo'), 'foo')

    def test_parse_number(self):
        self.assertEqual(tpl_parse('(1)'), [['val', 1]])

    def test_parse_string(self):
        self.assertEqual(tpl_parse('("string")'), [['val', 'string']])

    def test_parse_symbol(self):
        self.assertEqual(tpl_parse('(foo)'), ['foo'])

    def test_parse_nested_expression(self):
        self.assertEqual(tpl_parse('(foo (bar 1))'), ['foo', ['bar', ['val', 1]]])

    def test_parse_unbalanced_parenthesis(self):
        with self.assertRaises(Exception):
            tpl_parse('(foo')

    def test_parse_bad_parenthesis(self):
        with self.assertRaises(Exception):
            tpl_parse(')')

    def test_parse_empty_program(self):
        with self.assertRaises(Exception):
            tpl_parse('')

    def test_parse_trailing_garbage(self):
        with self.assertRaises(Exception):
            tpl_parse('foo bar')

    def test_eval_binary_operations(self):
        self.assertEqual(tpl_eval(tpl_parse('(+ 1 2)')), 3)
        self.assertEqual(tpl_eval(tpl_parse('(* 2 2)')), 4)
        self.assertEqual(tpl_eval(tpl_parse('(eq 1 1)')), True)
        self.assertEqual(tpl_eval(tpl_parse('(and true false)')), False)

    def test_eval_unary_operators(self):
        self.assertEqual(tpl_eval(tpl_parse('(not true)')), False)
        self.assertEqual(tpl_eval(tpl_parse('(- 1)')), -1)

    def test_eval_conditional(self):
        self.assertEqual(tpl_eval(tpl_parse('(? (lt 1 2) true false)')), True)

    def test_eval_print(self):
        self.assertEqual(tpl_eval(tpl_parse('(print "hello")')), None)

    def test_eval_empty_list(self):
        with self.assertRaises(ValueError):
            tpl_eval(tpl_parse('()'))

    def test_unknown_expression(self):
        with self.assertRaises(ValueError):
            tpl_eval(tpl_parse('(mod 2 3)'))

if __name__ == '__main__':
    unittest.main()
