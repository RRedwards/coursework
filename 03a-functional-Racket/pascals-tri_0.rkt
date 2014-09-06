;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-reader.ss" "lang")((modname pascals-tri_0) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ())))
;; Column Row -> PascalsTriValue
(check-expect (pascal 0 0) 1)
(check-expect (pascal 0 1) 1)
(check-expect (pascal 1 1) 1)
(check-expect (pascal 0 2) 1)
(check-expect (pascal 1 2) 2)
(check-expect (pascal 2 2) 1)
(check-expect (pascal 0 3) 1)
(check-expect (pascal 1 3) 3)
(check-expect (pascal 2 3) 3)
(check-expect (pascal 3 3) 1)
(check-expect (pascal 0 4) 1)
(check-expect (pascal 1 4) 4)
(check-expect (pascal 2 4) 6)
(check-expect (pascal 3 4) 4)
(check-expect (pascal 4 4) 1)

(define (pascal c r)
  (cond
    [(or (= r 0) (= c 0) (= r c)) 1]
    [else
     (+ (pascal (sub1 c) (sub1 r)) (pascal c (sub1 r)))]))


    