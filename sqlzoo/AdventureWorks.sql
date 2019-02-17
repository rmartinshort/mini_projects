/*
Easy questions
*/

/*
Q1
Show the first name and the email address of 
customer with CompanyName 'Bike World'
*/

SELECT FirstName, EmailAddress from Customer
WHERE CompanyName = 'Bike World'

/*
Q2
Show the CompanyName for all customers with an 
address in City 'Dallas'.
*/

SELECT CompanyName, City FROM Customer 
JOIN CustomerAddress ON CustomerAddress.CustomerID = Customer.CustomerID
JOIN Address ON Address.AddressID = CustomerAddress.AddressID
WHERE City LIKE '%Dallas%'

/*
Q3
How many items with ListPrice more than $1000 have been sold?
*/

SELECT SUM(OrderQty) FROM SalesOrderDetail 
JOIN Product ON Product.ProductID = SalesOrderDetail.ProductID
WHERE ListPrice > 1000

/*
Q4
Give the CompanyName of those customers with orders over 
$100000. Include the subtotal plus tax plus freight.
*/

SELECT CompanyName, SubTotal + TaxAmt + Freight as totalcost FROM Customer 
JOIN SalesOrderHeader ON SalesOrderHeader.CustomerID = Customer.CustomerID
WHERE SubTotal + TaxAmt + Freight > 100000

/*
Q5
Find the number of left racing socks 
('Racing Socks, L') ordered by CompanyName 'Riding Cycles'
*/

SELECT SUM(OrderQty) FROM SalesOrderDetail 
JOIN Product ON Product.ProductID = SalesOrderDetail.ProductID
JOIN SalesOrderHeader ON SalesOrderHeader.SalesOrderID = SalesOrderDetail.SalesOrderID
WHERE CustomerID IN (
SELECT CustomerID FROM Customer WHERE CompanyName = 'Riding Cycles'
)
AND Name = 'Racing Socks, L'

/*
Medium Questions
*/

/*
Q6
A "Single Item Order" is a customer order 
where only one item is ordered. Show the SalesOrderID 
and the UnitPrice for every Single Item Order.
*/ 

SELECT A.SalesOrderID, A.UnitPrice FROM SalesOrderDetail A
JOIN SalesOrderHeader B ON B.SalesOrderID = A.SalesOrderID
GROUP BY 1,2
HAVING SUM(OrderQty) = 1

/*
Q7
Where did the racing socks go? List the product name 
and the CompanyName for all Customers who ordered ProductModel 'Racing Socks'.
*/

SELECT prod.Name, cus.CompanyName FROM Product prod
JOIN SalesOrderDetail ON SalesOrderDetail.ProductID = prod.ProductID
JOIN SalesOrderHeader ON SalesOrderHeader.SalesOrderID = SalesOrderDetail.SalesOrderID
JOIN Customer cus ON cus.CustomerID = SalesOrderHeader.CustomerID
WHERE prod.ProductModelID = 
(
SELECT ProductModelID FROM ProductModel WHERE name = 'Racing Socks'
)

/*
Q8
Show the product description for culture 'fr' for product with ProductID 736.
*/

SELECT Description FROM ProductDescription 
JOIN ProductModelProductDescription pmpd On pmpd.ProductDescriptionID = 
ProductDescription.ProductDescriptionID 
JOIN ProductModel ON ProductModel.ProductModelID = pmpd.ProductModelID
JOIN Product ON Product.ProductModelID = ProductModel.ProductModelID
WHERE (culture = 'fr') AND (ProductID = '736')


/*
Q9
Use the SubTotal value in SaleOrderHeader to list orders from the largest 
to the smallest. For each order show the CompanyName and the SubTotal 
and the total weight of the order.
*/

SELECT CompanyName, SubTotal, SUM(OrderQty*Weight) as total_weight FROM SalesOrderHeader
JOIN Customer ON Customer.CustomerID = SalesOrderHeader.CustomerID
JOIN SalesOrderDetail ON SalesOrderDetail.SalesOrderID = SalesOrderHeader.SalesOrderID
JOIN Product ON Product.ProductID = SalesOrderDetail.ProductID
GROUP BY 1, 2

/*
Q10
How many products in ProductCategory 'Cranksets' 
have been sold to an address in 'London'?
*/
SELECT SUM(OrderQty) FROM SalesOrderDetail 
JOIN Product ON Product.ProductID = SalesOrderDetail.ProductID 
JOIN SalesOrderHeader ON SalesOrderHeader.SalesOrderID = SalesOrderDetail.SalesOrderID
WHERE ProductCategoryID = 
(
SELECT ProductCategoryID FROM ProductCategory WHERE Name = 'Cranksets'
)
AND BillToAddressID IN 
(
SELECT AddressID FROM Address WHERE city = 'London'
)


