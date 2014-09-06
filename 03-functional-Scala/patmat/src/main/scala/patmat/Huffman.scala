package patmat

import common._

/**
 * Assignment 4: Huffman coding
 *
 */
object Huffman {

  /**
   * A huffman code is represented by a binary tree.
   *
   * Every `Leaf` node of the tree represents one character of the alphabet that the tree can encode.
   * The weight of a `Leaf` is the frequency of appearance of the character.
   *
   * The branches of the huffman tree, the `Fork` nodes, represent a set containing all the characters
   * present in the leaves below it. The weight of a `Fork` node is the sum of the weights of these
   * leaves.
   */
  abstract class CodeTree
  case class Fork(left: CodeTree, right: CodeTree, chars: List[Char], weight: Int) extends CodeTree
  case class Leaf(char: Char, weight: Int) extends CodeTree

  //
  //  trait foo { println("foo") }
  //  trait bar { println("bar") }
  //  class foobar extends foo with bar
  //  
  //  abstract class Foo1 { val v = 1 }
  //  abstract class Bar1 { val z = 2 }
  //  class Foo1Bar1NoCompile extends Foo1 with Bar1
  //  

  // Part 1: Basics

  def weight(tree: CodeTree): Int = tree match {
    case Leaf(_, x) => x
    case Fork(l, r, c, w) => w
  }

  def chars(tree: CodeTree): List[Char] = tree match {
    case Leaf(x, _) => List(x)
    case Fork(l, r, c, w) => c
  }

  def makeCodeTree(left: CodeTree, right: CodeTree) =
    Fork(left, right, chars(left) ::: chars(right), weight(left) + weight(right))

  // Part 2: Generating Huffman trees

  /**
   * In this assignment, we are working with lists of characters. This function allows
   * you to easily create a character list from a given string.
   */
  def string2Chars(str: String): List[Char] = str.toList

  /**
   * This function computes for each unique character in the list `chars` the number of
   * times it occurs. For example, the invocation
   *
   *   times(List('a', 'b', 'a'))
   *
   * should return the following (the order of the resulting list is not important):
   *
   *   List(('a', 2), ('b', 1))
   *
   * The type `List[(Char, Int)]` denotes a list of pairs, where each pair consists of a
   * character and an integer. Pairs can be constructed easily using parentheses:
   *
   *   val pair: (Char, Int) = ('c', 1)
   *
   * In order to access the two elements of a pair, you can use the accessors `_1` and `_2`:
   *
   *   val theChar = pair._1
   *   val theInt  = pair._2
   *
   * Another way to deconstruct a pair is using pattern matching:
   *
   *   pair match {
   *     case (theChar, theInt) =>
   *       println("character is: "+ theChar)
   *       println("integer is  : "+ theInt)
   *   }
   */
  def times(chars: List[Char]): List[(Char, Int)] = {
    def timesAcc[G](chars: List[G], acc: List[(G, Int)] = Nil): List[(G, Int)] = chars match {
      case Nil => acc
      case x :: xs => timesAcc(xs, updateAccPG(x, acc))
    }
    //
    //    def updateAcc(char: Char, acc: List[(Char, Int)]): List[(Char, Int)] =
    //      if (acc == Nil) List((char, 1))
    //      else if (acc.head._1 == char) (acc.head._1, acc.head._2 + 1) :: acc.tail
    //      else acc.head :: updateAcc(char, acc.tail)

    def updateAccPG[G](g: G, acc: List[(G, Int)]): List[(G, Int)] = acc match {
      case Nil => List(g -> 1)
      case (c, n) :: t if c == g => (g, n + 1) :: t
      case h :: t => h :: updateAccPG(g, t)
    }

    timesAcc(chars)
  }

  /**
   * Returns a list of `Leaf` nodes for a given frequency table `freqs`.
   *
   * The returned list should be ordered by ascending weights (i.e. the
   * head of the list should have the smallest weight), where the weight
   * of a leaf is the frequency of the character.
   */
  def makeOrderedLeafList(freqs: List[(Char, Int)]): List[Leaf] = {
    def makeLeaf(t: (Char, Int)): Leaf = Leaf(t._1, t._2)
    freqs sortBy (_._2) map makeLeaf
  }

  //  def makeLeaf = (Leaf.apply _).tupled

  /**
   * Checks whether the list `trees` contains only one single code tree.
   */
  def singleton(trees: List[CodeTree]): Boolean = trees match {
    case List(_) => true
    case _ => false
  }

  /**
   * The parameter `trees` of this function is a list of code trees ordered
   * by ascending weights.
   *
   * This function takes the first two elements of the list `trees` and combines
   * them into a single `Fork` node. This node is then added back into the
   * remaining elements of `trees` at a position such that the ordering by weights
   * is preserved.
   *
   * If `trees` is a list of less than two elements, that list should be returned
   * unchanged.
   */
  def combine(trees: List[CodeTree]): List[CodeTree] = trees match { //???
    case x if x.length <= 1 => x
    case y :: z => makeCodeTree(y, z.head) :: z.tail sortBy (weight)
  }
  //
  //  def combineP(trees: List[CodeTree]): List[CodeTree] = trees match { //???
  //    case List(_) | Nil => trees
  //    case y :: z => makeCodeTree(y, z.head) :: z.tail sortBy (weight)
  //  }

  /**
   * This function will be called in the following way:
   *
   *   until(singleton, combine)(trees)
   *
   * where `trees` is of type `List[CodeTree]`, `singleton` and `combine` refer to
   * the two functions defined above.
   *
   * In such an invocation, `until` should call the two functions until the list of
   * code trees contains only one single tree, and then return that singleton list.
   *
   * Hint: before writing the implementation,
   *  - start by defining the parameter types such that the above example invocation
   *    is valid. The parameter types of `until` should match the argument types of
   *    the example invocation. Also define the return type of the `until` function.
   *  - try to find sensible parameter names for `xxx`, `yyy` and `zzz`.
   */

  def until(sfn: List[CodeTree] => Boolean, cfn: List[CodeTree] => List[CodeTree])(trees: List[CodeTree]): CodeTree =
    if (sfn(trees)) trees.head
    else until(sfn, cfn)(cfn(trees))

  //  def until(xxx: ???, yyy: ???)(zzz: ???): ??? = ???

  /**
   * This function creates a code tree which is optimal to encode the text `chars`.
   *
   * The parameter `chars` is an arbitrary text. This function extracts the character
   * frequencies from that text and creates a code tree based on them.
   */
  def createCodeTree(chars: List[Char]): CodeTree =
    until(singleton, combine)(makeOrderedLeafList(times(chars)))

  //  // crazy more stuff 
  //  val createCodeTreePointFree =
  //    times _ andThen makeOrderedLeafList _ andThen until(singleton, combine) _
  //
  //  // and even crazy moar sterf
  //  def giveMeHead[T](xs: List[T]) = xs.head
  //  val createCodPeace =
  //    times _ andThen makeOrderedLeafList _ andThen untilFixed(singleton, combine) _ andThen giveMeHead _
  //
  //  def untilFixed[T](sfn: T => Boolean, cfn: T => T)(t: T): T =
  //    if (sfn(t)) t
  //    else untilFixed(sfn, cfn)(cfn(t))

  // Part 3: Decoding

  type Bit = Int

  /**
   * This function decodes the bit sequence `bits` using the code tree `tree` and returns
   * the resulting list of characters.
   */
  def decode(tree: CodeTree, bits: List[Bit]): List[Char] = { //???

    def getLeft(tree: CodeTree): CodeTree = tree match {
      case Fork(l, r, c, w) => l
    }

    def getRight(tree: CodeTree): CodeTree = tree match {
      case Fork(l, r, c, w) => r
    }

    def decodeAcc(tree: CodeTree, wt: CodeTree, bits: List[Bit], acc: List[Char]): List[Char] =
      //    based on head of bit list, calls helper fn to look in left or right tree for Leaf
      //    assume that CodeTree is NOT a single Leaf, but is a Fork at root node
      if (bits == Nil) acc.reverse
      else if (bits.head == 0) addLeafToAcc(tree, getLeft(wt), bits.tail, acc)
      else if (bits.head == 1) addLeafToAcc(tree, getRight(wt), bits.tail, acc)
      else throw new Error("Bit List contained Int other than 0 or 1")

    def addLeafToAcc(fulltree: CodeTree, parttree: CodeTree, bits: List[Bit], acc: List[Char]): List[Char] = parttree match {
      case Leaf(c, _) => decodeAcc(fulltree, fulltree, bits, c :: acc)
      case Fork(_, _, _, _) => decodeAcc(fulltree, parttree, bits, acc)
    }
    decodeAcc(tree, tree, bits, Nil)
  }

  // Solved using a closure and pattern matching
  def decode2(tree: CodeTree, bits: List[Bit]): List[Char] = {

    def decodeAux(wt: CodeTree, bits: List[Bit], acc: List[Char]): List[Char] = {
      (bits, wt) match {
        case (_, Leaf(c, _)) => decodeAux(tree, bits, c :: acc)
        case (0 :: t, f: Fork) => decodeAux(f.left, t, acc)
        case (1 :: t, f: Fork) => decodeAux(f.right, t, acc)
        case (Nil, _) => acc.reverse
        case _ => throw new Error("This aint no two bit integer!")
      }
    }

    decodeAux(tree, bits, Nil)
  }

  /**
   * A Huffman coding tree for the French language.
   * Generated from the data given at
   *   http://fr.wikipedia.org/wiki/Fr%C3%A9quence_d%27apparition_des_lettres_en_fran%C3%A7ais
   */
  val frenchCode: CodeTree = Fork(Fork(Fork(Leaf('s', 121895), Fork(Leaf('d', 56269), Fork(Fork(Fork(Leaf('x', 5928), Leaf('j', 8351), List('x', 'j'), 14279), Leaf('f', 16351), List('x', 'j', 'f'), 30630), Fork(Fork(Fork(Fork(Leaf('z', 2093), Fork(Leaf('k', 745), Leaf('w', 1747), List('k', 'w'), 2492), List('z', 'k', 'w'), 4585), Leaf('y', 4725), List('z', 'k', 'w', 'y'), 9310), Leaf('h', 11298), List('z', 'k', 'w', 'y', 'h'), 20608), Leaf('q', 20889), List('z', 'k', 'w', 'y', 'h', 'q'), 41497), List('x', 'j', 'f', 'z', 'k', 'w', 'y', 'h', 'q'), 72127), List('d', 'x', 'j', 'f', 'z', 'k', 'w', 'y', 'h', 'q'), 128396), List('s', 'd', 'x', 'j', 'f', 'z', 'k', 'w', 'y', 'h', 'q'), 250291), Fork(Fork(Leaf('o', 82762), Leaf('l', 83668), List('o', 'l'), 166430), Fork(Fork(Leaf('m', 45521), Leaf('p', 46335), List('m', 'p'), 91856), Leaf('u', 96785), List('m', 'p', 'u'), 188641), List('o', 'l', 'm', 'p', 'u'), 355071), List('s', 'd', 'x', 'j', 'f', 'z', 'k', 'w', 'y', 'h', 'q', 'o', 'l', 'm', 'p', 'u'), 605362), Fork(Fork(Fork(Leaf('r', 100500), Fork(Leaf('c', 50003), Fork(Leaf('v', 24975), Fork(Leaf('g', 13288), Leaf('b', 13822), List('g', 'b'), 27110), List('v', 'g', 'b'), 52085), List('c', 'v', 'g', 'b'), 102088), List('r', 'c', 'v', 'g', 'b'), 202588), Fork(Leaf('n', 108812), Leaf('t', 111103), List('n', 't'), 219915), List('r', 'c', 'v', 'g', 'b', 'n', 't'), 422503), Fork(Leaf('e', 225947), Fork(Leaf('i', 115465), Leaf('a', 117110), List('i', 'a'), 232575), List('e', 'i', 'a'), 458522), List('r', 'c', 'v', 'g', 'b', 'n', 't', 'e', 'i', 'a'), 881025), List('s', 'd', 'x', 'j', 'f', 'z', 'k', 'w', 'y', 'h', 'q', 'o', 'l', 'm', 'p', 'u', 'r', 'c', 'v', 'g', 'b', 'n', 't', 'e', 'i', 'a'), 1486387)

  /**
   * What does the secret message say? Can you decode it?
   * For the decoding use the `frenchCode' Huffman tree defined above.
   */
  val secret: List[Bit] = List(0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1)

  /**
   * Write a function that returns the decoded secret
   */
  def decodedSecret: List[Char] = decode(frenchCode, secret)

  // Part 4a: Encoding using Huffman tree

  /**
   * This function encodes `text` using the code tree `tree`
   * into a sequence of bits.
   */
  def encode(tree: CodeTree)(text: List[Char]): List[Bit] = { //???

    def encodeAux(wtree: CodeTree, text: List[Char], acc: List[Bit]): List[Bit] = {
      (text, wtree) match {
        case (_, Leaf(_, _)) => encodeAux(tree, text.tail, acc)
        case (h :: t, Fork(l, r, _, _)) => if (chars(l).contains(h)) encodeAux(l, text, 0 :: acc) else encodeAux(r, text, 1 :: acc)
        case (Nil, _) => acc.reverse
        case _ => throw new Error("Uhhh...probably using wrong codetree for text")
      }
    }
    encodeAux(tree, text, Nil)
  }

  //  def retoad(tree: CodeTree): List[Char] => List[Bit] = {
  //    val map = Map() // takes time, so only doing once    
  //    text: List[Char] => { // returning a closure that can access my map      
  //      List()
  //    }
  //  }

  // Part 4b: Encoding using code table

  type CodeTable = List[(Char, List[Bit])]

  /**
   * This function returns the bit sequence that represents the character `char` in
   * the code table `table`.
   */
  def codeBits(table: CodeTable)(char: Char): List[Bit] = table match { //???
    case (x, bits) :: t => if (x == char) bits else codeBits(t)(char)
    case Nil => throw new Error("couldn't find char in code table")
  }

  /**
   * Given a code tree, create a code table which contains, for every character in the
   * code tree, the sequence of bits representing that character.
   *
   * Hint: think of a recursive solution: every sub-tree of the code tree `tree` is itself
   * a valid code tree that can be represented as a code table. Using the code tables of the
   * sub-trees, think of how to build the code table for the entire tree.
   */
  //  def convertZZZ(tree: CodeTree): CodeTable = { //???

  //   def convertAux(wtree: CodeTree, chars: List[Char], acc: CodeTable): CodeTable = 
  //	(chars, wtree) match {
  //      	case (Nil, _)                   => acc
  //      	case (Leaf(c, _))       => List((c, Nil))
  //      	case (Fork(l, r, c, _)) => mergeCodeTables(convertAux(l, 0 :: ???), convertAux(r, ???))
  //   }
  //     convertAux(tree, chars(tree), map ???)
  //    ???
  //  }
  ////  when it gets to a Leaf(c, _), return a code table like List((c, Nil))
  //  when merging code tables, 0's or 1's get cons'ed onto ^

  /**
   * This function takes two code tables and merges them into one. Depending on how you
   * use it in the `convert` method above, this merge method might also do some transformations
   * on the two parameter code tables.
   */
  def mergeCodeTables(a: CodeTable, b: CodeTable): CodeTable = a //???
  //    (a, b) match {
  //    case (Nil, b) => b
  //    case (a, Nil) => a
  //    case (List(c1, b1), List(c2, b2)) => List(???)
  //  }

  /**
   * This function encodes `text` according to the code tree `tree`.
   *
   * To speed up the encoding process, it first converts the code tree to a code table
   * and then uses it to perform the actual encoding.
   */
  def quickEncode(tree: CodeTree)(text: List[Char]): List[Bit] = {

    def quickEncodeAux(table: CodeTable, text: List[Char], acc: List[Bit]): List[Bit] = text match {
      case Nil => acc.reverse
      case h :: t => quickEncodeAux(table, t, codeBits(table)(h).reverse ::: acc)
    }
    quickEncodeAux(convert(tree), text, Nil)
  }

  //  def quickEncode2(tree: CodeTree) = {
  //    val lookup = codeBits(convert(tree)) _
  //    (text:List[Char]) => text map lookup
  //  }
  //  
  //  

  //  Don't mind me, I'm just some random scribbling...
  def convert(tree: CodeTree): CodeTable = {

    def convertAux(wtree: CodeTree, xs: List[Char], accOuter: CodeTable, accInner: CodeTable): CodeTable =
      (wtree, xs) match {
        case (_, Nil) => accOuter
        case (Leaf(c, _), h :: t) => convertAux(tree, t, accInner ::: accOuter, Nil)
        case (Fork(l, r, c, _), h :: t) =>
          if (chars(l).contains(h)) convertAux(l, xs, accOuter, updateCT(h, 0, accInner))
          else convertAux(r, xs, accOuter, updateCT(h, 1, accInner))
        case _ => throw new Error("Hi Martin!")
      }

    def updateCT(char: Char, bit: Bit, accInner: CodeTable): CodeTable = accInner match {
      case Nil => List((char, List(bit)))
      case List((x, bs)) => if (x == char) List((char, bs ::: List(bit))) else throw new Error
    }

    convertAux(tree, chars(tree), Nil, Nil) //List[(Char, List[Bit])]
  }
  //    List((chars(tree).head, Nil))
}


