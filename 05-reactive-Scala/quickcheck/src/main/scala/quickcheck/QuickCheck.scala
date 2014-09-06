package quickcheck

import common._

import org.scalacheck._
import Arbitrary._
import Gen._
import Prop._

abstract class QuickCheckHeap extends Properties("Heap") with IntHeap {

//  property("min1") = forAll { a: Int =>
//    val h = insert(a, empty)
//    findMin(h) == a
//  }
//
//  property("delete min of 1") = forAll { a: Int => //???
//    val h = insert(a, empty)
//    deleteMin(h) == empty
//  }
//
//  property("min of 2") = forAll { (a: Int, b: Int) => //???
//    val h = insert(b, insert(a, empty))
//    findMin(h) == List(a, b).min
//  }
//
//  property("minOfmelding2") = forAll { (h1: H, h2: H) => //???
//    val m = findMin(meld(h1, h2))
//    (m == findMin(h1)) || (m == findMin(h2))
//  }

  property("result of emptying heap should be sorted") = forAll { (a: Int, b: Int, c: Int) => //???
    val xs = List(a, b, c).sorted(Ordering[Int].reverse)
    val h  = meld(insert(b, insert(a, empty)), insert(c, empty))
    val ys = heapToList(h)
    ys == xs
  }

  //    property("associative order of insert & meld") = forAll { (a: Int, h1: H, h2: H) =>  //???
  //      insert(a, meld(h1, h2)) == meld(h1, insert(a, h2))
  //    }

  def heapToList(h: H, acc: List[A] = Nil): List[A] = //???
    if (isEmpty(h)) acc
    else heapToList(deleteMin(h), findMin(h) :: acc)
    
  def heapToList2(h: H): List[A] =
    if (isEmpty(h)) Nil
    else findMin(h) :: heapToList2(deleteMin(h))

  lazy val genHeap: Gen[H] = //???
    for {
      h <- arbitrary[Int]
      t <- oneOf(value(empty), genHeap)
    } yield insert(h, t)
  //    oneOf(emptyHeaps, nonEmptyHeaps)

  //  def emptyHeaps: Gen[H] = value(empty)
  //  
  //  def nonEmptyHeaps: Gen[H] = for {  //???
  //     h <- arbitrary[Int]
  //     t <- genHeap
  //  } yield insert(h, t)

  implicit lazy val arbHeap: Arbitrary[H] = Arbitrary(genHeap)

}
