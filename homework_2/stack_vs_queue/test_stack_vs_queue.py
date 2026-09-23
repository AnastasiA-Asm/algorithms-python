import unittest

from stack_vs_queue import Queue, Stack

class TestStack(unittest.TestCase):
    def test_stack_order_and_peek(self):
        stack = Stack()
        stack.push(18)
        stack.push(7)
        stack.push(-4)

        self.assertEqual(stack.peek(), -4)
        self.assertEqual(stack.peek(), -4)

        self.assertEqual(stack.pop(), -4)
        self.assertEqual(stack.pop(), 7)
        self.assertEqual(stack.pop(), 18)
        self.assertTrue(stack.is_empty())

    def test_stack_mixed_operations_and_reuse(self):
        stack = Stack()
        stack.push(5)
        stack.push(5)

        self.assertEqual(stack.pop(), 5)

        stack.push(0)
        stack.push(-3)

        self.assertEqual(stack.pop(), -3)
        self.assertEqual(stack.pop(), 0)
        self.assertEqual(stack.pop(), 5)

        # Проверяем что опустевший стек можно использовать снова
        stack.push(42)
        self.assertEqual(stack.pop(), 42)
        self.assertTrue(stack.is_empty())

    def test_empty_stack_errors(self):
        stack = Stack()

        self.assertTrue(stack.is_empty())

        with self.assertRaises(IndexError):
            stack.pop()

        with self.assertRaises(IndexError):
            stack.peek()

class TestQueue(unittest.TestCase):
    def test_queue_order_and_peek(self):
        queue = Queue()
        queue.enqueue(18)
        queue.enqueue(7)
        queue.enqueue(-4)

        self.assertEqual(queue.peek(), 18)
        self.assertEqual(queue.peek(), 18)

        self.assertEqual(queue.dequeue(), 18)
        self.assertEqual(queue.dequeue(), 7)
        self.assertEqual(queue.dequeue(), -4)
        self.assertTrue(queue.is_empty())

    def test_queue_mixed_operations_and_reuse(self):
        queue = Queue()
        queue.enqueue(5)
        queue.enqueue(5)

        self.assertEqual(queue.dequeue(), 5)

        queue.enqueue(-3)
        queue.enqueue(0)

        self.assertEqual(queue.dequeue(), 5)
        self.assertEqual(queue.dequeue(), -3)
        self.assertEqual(queue.dequeue(), 0)

        # Здесь очередь уже пустая. Проверяем особый случай:
        # head и tail должны позволить снова добавить элемент
        queue.enqueue(42)

        self.assertEqual(queue.peek(), 42)
        self.assertEqual(queue.dequeue(), 42)
        self.assertTrue(queue.is_empty())

    def test_empty_queue_errors(self):
        queue = Queue()

        self.assertTrue(queue.is_empty())

        with self.assertRaises(IndexError):
            queue.dequeue()

        with self.assertRaises(IndexError):
            queue.peek()

if __name__ == "__main__":
    unittest.main()