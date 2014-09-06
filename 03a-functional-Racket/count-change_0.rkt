;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-reader.ss" "lang")((modname count-change_0) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ())))
;; Integer (listof Integer) -> Integer
;; counts how many different ways you can make change for an amount, given a list of coin denominations
(check-expect (countChange 4 empty) 0)
(check-expect (countChange 4 (list 1)) 1)
(check-expect (countChange 4 (list 2)) 1)
(check-expect (countChange 4 (list 1 2)) 3)
(check-expect (countChange 4 (list 2 1)) 3)
(check-expect (countChange 10 (list 1 10 5)) 4)
(check-expect (countChange 10 (list 5 1)) 3)
(check-expect (countChange 300 (list 500 5 50 100 20 200 10)) 1022)


(define (countChange money coins)
  (cond
    [(= money 0) 1]
    [(empty? coins) 0]
    [(< money 0) 0]
    [else
     (+ (countChange (- money (first coins)) coins)
        (countChange money (rest coins)))]))


;;---------------------
(define (sortList loi)
  (cond [(empty? loi) empty]
        [else
         (insert (first loi)
                 (sortList (rest loi)))]))

(define (insert i loi)
  (cond [(empty? loi) (cons i empty)]
        [else
         (if (< i (first loi))
             (cons (first loi) (insert i (rest loi)))
             (cons i loi))]))