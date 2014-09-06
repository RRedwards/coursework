;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-reader.ss" "lang")((modname sort-and-max-wksht) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ())))
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

(sortList (list 0 5 3 4 1 2))


(define (maxList lst) (maxAuxList (first lst) (rest lst)))

(define (maxAuxList cur lst)
  (cond [(empty? lst) cur]
        [(> cur (first lst)) (maxAuxList cur (rest lst))]
        [else (maxAuxList (first lst) (rest lst))]))