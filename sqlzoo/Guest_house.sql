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
Ruth Cadbury. Show the total amount payable by guest Ruth Cadbury 
for her room bookings. You should JOIN to the rate table using room_type_requested and occupants.
*/ 

SELECT SUM(nights*A.amount) FROM
booking JOIN rate A on A.room_type = booking.room_type_requested AND A.occupancy = booking.occupants
WHERE guest_id = ( 
SELECT id FROM guest WHERE first_name = 'Ruth' AND last_name = 'Cadbury'
)

/*
Q7
Including Extras. Calculate the total bill for booking 5346 including extras
Note here the ability to just add sums from other tables without needed to join them!
*/

SELECT SUM(A.amount) + (
SELECT SUM(amount)
FROM extra
WHERE booking_id = 5346
) as sum_amount
FROM
booking B JOIN rate A on A.room_type = B.room_type_requested AND A.occupancy = B.occupants
WHERE booking_id = 5346


/*
Q8
Edinburgh Residents. For every guest who has the word “Edinburgh” in their 
address show the total number of nights booked. Be sure to include 0 for those 
guests who have never had a booking. Show last name, first name, address and number 
of nights. Order by last name then first name.

Note the use of COALESCE here to force the sum column to be zero where its NULL
*/

SELECT A.last_name as last_name, A.first_name as first_name, A.address as address, COALESCE(SUM(nights),0) as nnights
FROM guest A LEFT JOIN booking B ON (A.id = B.guest_id)
WHERE address LIKE '%Edinburgh%'
GROUP BY last_name, first_name, address
ORDER BY last_name, first_name


/*
How busy are we? For each day of the week beginning 2016-11-25 show the number of bookings 
starting that day. Be sure to show all the days of the week in the correct order.
*/

SELECT booking_date, COUNT(booking_id) FROM booking
GROUP BY booking_date
HAVING booking_date IN ('2016-11-25','2016-11-26','2016-11-27','2016-11-28','2016-11-29',
	'2016-11-30','2016-12-01')
