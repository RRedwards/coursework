package simulations

import math.random

class EpidemySimulator extends Simulator {

  def randomBelow(i: Int) = (random * i).toInt

  protected[simulations] object SimConfig {
    val population: Int = 300
    val roomRows: Int = 8
    val roomColumns: Int = 8

    // to complete: additional parameters of simulation
    val initInfectRate = 0.01
    val transmitRate = 0.4
    val fatalityRate = 0.25

    // action delays
    val incubDelay = 6
    val deathDelay = 14
    val immuneDelay = 16
    val recoveryDelay = 18
  }

  import SimConfig._

  val persons: List[Person] = { // ??? to complete: construct list of persons

    val initInfectNum = (population * initInfectRate).toInt

    val peeps: List[Person] = {
      for (id <- (1 to population).toList) yield new Person(id)
      //      (1 to population) map(i=>new Person(i)) toList
    }
    //    for (p <- peeps.take(initInfectNum)) { p.infected = true }
    peeps take (initInfectNum) foreach { _.infected = true }

    peeps
  }

  class Person(val id: Int) {
    var infected = false
    var sick = false
    var immune = false
    var dead = false

    // demonstrates random number generation
    var row: Int = randomBelow(roomRows)
    var col: Int = randomBelow(roomColumns)

    //
    // to complete with simulation logic
    //

    def nearRooms(row: Int, col: Int): List[(Int, Int)] = List(
      /* down  */ ((row + 1) % roomRows, col),
      /* up    */ (if (row > 0) (row - 1, col) else (roomRows - 1, col)),
      /* left  */ (if (col > 0) (row, col - 1) else (row, roomColumns - 1)),
      /* right */ (row, (col + 1) % roomColumns))

    def safeRooms(peeps: List[Person], rooms: List[(Int, Int)]) = { //???
      val sickPeeps = peeps filter (p => (p.sick | p.dead))
      val sickRooms = (for (p <- sickPeeps) yield (p.row, p.col)).distinct
      rooms filterNot (sickRooms contains _)
    }

    def exposed = persons exists (p => p.row == row && p.col == col && p.infected)

    def caughtContagion = math.random < transmitRate

    def pickRoom() = safeRooms(persons, nearRooms(row, col)) match {
      case Nil =>
      case xs =>
        val (r, c) = xs(randomBelow(xs.length))
        row = r; col = c
    }

    def moveGate(w: Wire, out: Wire) {
      def moveAction() {
        val v = randomBelow(5) + 1
        afterDelay(v) {
          if (!dead) pickRoom()
          if (exposed & caughtContagion) {
            infected = true
            out setSignal infected
          }
          if (!dead) moveGate(w, out)
        }
      }
      w addAction moveAction
    }

    def incubationGate(incubationWire: Wire) {
      def incubationAction() = afterDelay(incubDelay) {
        if (!dead) sick = true
      }
      incubationWire addAction incubationAction
    }
    
    def deathGate(infectionWire: Wire) {
      def deathAction() = afterDelay(deathDelay) {
        if (math.random < fatalityRate) dead = true
      }
      infectionWire addAction deathAction
    }

    def immuneGate(infectionWire: Wire) {
      def immuneAction() = afterDelay(immuneDelay) {
        if (!dead) {
          immune = true
          sick = false
        }
      }
      infectionWire addAction immuneAction
    }

    def recoveredGate(infectionWire: Wire) {
      def recoveredAction() = afterDelay(recoveryDelay) {
        if (!dead) {
          infected = false
          immune = false
        }
      }
      infectionWire addAction recoveredAction
    }

    val moveWire, infectionWire = new Wire
    moveGate(moveWire, infectionWire)
    
    infectionWire setSignal infected
    incubationGate(infectionWire)
    deathGate(infectionWire)
    immuneGate(infectionWire)
    recoveredGate(infectionWire)
  }
}
