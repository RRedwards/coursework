package patmat

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

import patmat.Huffman._

@RunWith(classOf[JUnitRunner])
class HuffmanSuite extends FunSuite {
  trait TestTrees {
    val t1 = Fork(Leaf('a',2), Leaf('b',3), List('a','b'), 5)
    val t2 = Fork(Fork(Leaf('a',2), Leaf('b',3), List('a','b'), 5), Leaf('d',4), List('a','b','d'), 9)
  }

  test("weight of a larger tree") {
    new TestTrees {
      assert(weight(t1) === 5)
    }
  }

  test("chars of a larger tree") {
    new TestTrees {
      assert(chars(t2) === List('a','b','d'))
    }
  }

  test("string2chars(\"hello, world\")") {
    assert(string2Chars("hello, world") === List('h', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd'))
  }

  test("makeOrderedLeafList for some frequency table") {
    assert(makeOrderedLeafList(List(('t', 2), ('e', 1), ('x', 3))) === List(Leaf('e',1), Leaf('t',2), Leaf('x',3)))
  }
  
  test("makeOrderedLeafList 2nd test (...oops)") {
    new TestTrees {
      assert(makeOrderedLeafList(List(('a', 2), ('b', 1))) === List(Leaf('b', 1), Leaf('a', 2)))
    }
  }

  test("combine of some leaf list") {
    val leaflist = List(Leaf('e', 1), Leaf('t', 2), Leaf('x', 4))
    assert(combine(leaflist) === List(Fork(Leaf('e',1),Leaf('t',2),List('e', 't'),3), Leaf('x',4)))
  }

  test("decode and encode a very short text should be identity") {
    new TestTrees {
      assert(decode(t1, encode(t1)("ab".toList)) === "ab".toList)
      assert(encode(frenchCode)(decode(frenchCode, secret)) == secret)
    }
  }
  
  test("quickencode a very short text should be identity") {
    new TestTrees {
      assert(quickEncode(frenchCode)(decode(frenchCode, secret)) == secret)
    }
  }
    
  test("times works") {
    new TestTrees {
      assert(times(List('a', 'b', 'a')) === List(('a', 2), ('b', 1)))
    }
  }
  
//  test("makeLeaf works") {
//    new TestTrees {
//      assert(makeLeaf(('a', 2)) === Leaf('a', 2))
//    }
//  }
  
  test("codeBits works with simple imaginary code table") {
    val ct1 = List(('a', List(0, 1, 0, 1)), ('b', List(1, 1, 1, 1)))  //List[(Char, List[Bit])]
    assert(codeBits(ct1)('b') === List(1, 1, 1, 1))
  }
  
}
