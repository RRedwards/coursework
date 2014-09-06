package funsets

object W2_Lect5_Data {
  val x = new Rational(1, 2)
	x.numer
}

class Rational(x: Int, y: Int) {
  def numer = x
  def denom = y
}