package simulations

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class CircuitSuite extends CircuitSimulator with FunSuite {
  val InverterDelay = 1
  val AndGateDelay = 3
  val OrGateDelay = 5

  test("andGate example") {
    val in1, in2, out = new Wire
    andGate(in1, in2, out)
    in1.setSignal(false)
    in2.setSignal(false)
    run

    assert(out.getSignal === false, "and 1")

    in1.setSignal(true)
    run

    assert(out.getSignal === false, "and 2")

    in2.setSignal(true)
    run

    assert(out.getSignal === true, "and 3")
  }

  //
  // to complete with tests for orGate, demux, ...
  //

  test("demux 0 control, 1 output") {
    val in, out = new Wire
    demux(in, Nil, List(out))
    in.setSignal(true)
    run
    assert(out.getSignal === true, "demux 0, t")

    in.setSignal(false)
    run
    assert(out.getSignal === false, "demux 0, f")

  }

  test("demux 1 control, 2 output") {
    val in, c, outL, outR = new Wire
    demux(in, List(c), List(outL, outR))
    in.setSignal(true)
    c.setSignal(true)
    run
    assert(outL.getSignal === true, "demux 1, outL 1")
    assert(outR.getSignal === false, "demux 1, outR 1")

    c.setSignal(false)
    run
    assert(outL.getSignal === false, "demux 1, outL 2")
    assert(outR.getSignal === true, "demux 1, outR 2")
  }

  test("demux 2 control, 4 output") {
    val in, c1, c2, o1, o2, o3, o4 = new Wire
    demux(in, List(c1, c2), List(o1, o2, o3, o4))
    in.setSignal(true)
    run
    assert(o1.getSignal === false, "demux 2, o1 1")
    assert(o2.getSignal === false)
    assert(o3.getSignal === false)
    assert(o4.getSignal === true)

    c2.setSignal(true)
    run
    assert(o1.getSignal === false)
    assert(o2.getSignal === false)
    assert(o3.getSignal === true)
    assert(o4.getSignal === false)
    
    c1.setSignal(true)
    run
    assert(o1.getSignal === true)
    assert(o2.getSignal === false)
    assert(o3.getSignal === false)
    assert(o4.getSignal === false)
  }
}
