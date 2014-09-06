package recfun
import common._

object Main {
  def main(args: Array[String]) {
    println("Pascal's Triangle")
    for (row <- 0 to 10) {
      for (col <- 0 to row)
        print(pascal(col, row) + " ")
      println()
    }
  }

  /**
   * Exercise 1
   */
  def pascal(c: Int, r: Int): Int = 
    if ((c == 0) || (r == c)) 1
    else (pascal((c - 1), (r - 1)) + pascal(c, (r - 1)))

//    
//    implicit class Foo(i: Int) {
//       def inc = i + 1 
//       def dec = i -1
//    }
  /**
   * Exercise 2
   */
  def balance(chars: List[Char]): Boolean = {
      
    def balAux(chars: List[Char], count: Int = 0): Boolean = 
       if (chars.isEmpty) count == 0
       else if (count < 0) false
       else if (chars.head == '(') balAux(chars.tail, count + 1)
       else if (chars.head == ')') balAux(chars.tail, count - 1)
       else balAux((chars.tail), count) 
              
    balAux(chars)
  }
  
  /**
   * Exercise 3
   */
  def countChange(money: Int, coins: List[Int]): Int = 
    if (money == 0) 1
    else if (coins.isEmpty) 0
    else if (money < 0) 0
    else    (countChange(money - coins.head, coins)) + (countChange(money, coins.tail))
    
}
