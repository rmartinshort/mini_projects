/*
Easy questions
*/

/*
Q1
Guest 1183. Give the booking_date and the number of nights for guest 1183.
*/

SELECT first_name,last_name
FROM booking JOIN guest ON guest_id = guest.id
 WHERE room_no=101 AND booking_date='2016-11-17'

/*
Q2
When do they get here? List the arrival time and the first and 
last names for all guests due to arrive on 2016-11-05, order the output by time of arrival.
*/

SELECT arrival_time, first_name, last_name FROM booking
JOIN guest ON (booking.guest_id = guest.id)
WHERE booking_date = '2016-11-05'
ORDER BY arrival_time

/*
Q3
Look up daily rates. Give the daily rate that should be paid for bookings with 
ids 5152, 5165, 5154 and 5295. Include booking id, room type, number of occupants and the amount.
*/

SELECT  booking_id, room_type_requested, occupants, amount FROM booking
JOIN rate on (rate.room_type = booking.room_type_requested) 
WHERE booking_id IN ('5152','5165','5154','5295')

/*
Q4
List the number of images taken by each camera. Your answer should show how many images have been taken by camera 1, camera 2 etc. 
The list must NOT include the images taken by camera 15, 16, 17, 18 and 19.
*/

SELECT camera, COUNT(*) FROM image 
GROUP BY camera
HAVING camera < 15

/*
Q5
Who’s in 101? Find who is staying in room 101 on 2016-12-03, include first name, last name and address.
*/

SELECT first_name, last_name, address FROM guest
JOIN booking ON (booking.guest_id = guest.id)
WHERE booking_date = '2016-12-03' AND room_no = 101

/*
Q6
