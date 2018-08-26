/*
Easy questions
*/

/*
Q1
Show the name and address of the keeper of vehicle SO 02 PSP.
*/

SELECT name, address, vehicle.id FROM keeper 
JOIN vehicle ON (vehicle.keeper = keeper.id)
WHERE vehicle.id = 'SO 02 PSP'

/*
Q2
Show the number of cameras that take images for incoming vehicles.
*/

SELECT COUNT(*) FROM camera

/*
Q3
List the image details taken by Camera 10 before 26 Feb 2007.
*/

SELECT * FROM image 
WHERE (camera = 10) AND (whn < '2007-02-26')

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
A number of vehicles have permits that start on 30th Jan 2007. 
List the name and address for each keeper in alphabetical order without duplication.
*/

SELECT DISTINCT name, address FROM keeper
JOIN vehicle on (vehicle.keeper = keeper.id)
JOIN permit on (permit.reg = vehicle.id)
WHERE permit.SDate = '2007-01-30'
