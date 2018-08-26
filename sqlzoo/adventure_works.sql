/*
Easy questions
*/

/*
Q1
Show the first name and the email address of customer with CompanyName 'Bike World'
*/

SELECT FirstName, EmailAddress FROM Customer
WHERE CompanyName = 'Bike World'


/*
Q2
Show the CompanyName for all customers with an address in City 'Dallas'.
*/

SELECT CompanyName, City FROM Customer
JOIN CustomerAddress ON (CustomerAddress.CustomerID = Customer.CustomerID)
JOIN Address ON (Address.AddressID  = CustomerAddress.AddressID)
WHERE City = 'Dallas'

/*
Q3
How many items with ListPrice more than $1000 have been sold?
*/

SELECT COUNT(ProductID) FROM Product
WHERE ListPrice > 1000

/*
Q4
Give the CompanyName of those customers with orders over $100000. 
Include the subtotal plus tax plus freight.
*/

SELECT CompanyName FROM Customer
JOIN SalesOrderHeader ON (SalesOrderHeader.CustomerID = Customer.CustomerID) 
WHERE (Subtotal + TaxAmt + Freight) > 100000

/*
Q5
Find the number of left racing socks ('Racing Socks, L') 
ordered by CompanyName 'Riding Cycles'
*/

SELECT SUM(OrderQty) FROM SalesOrderDetail 
JOIN Product ON (Product.ProductID  = SalesOrderDetail.ProductID)
JOIN SalesOrderHeader ON (SalesOrderHeader.SalesOrderID = SalesOrderDetail.SalesOrderID)
JOIN Customer ON (SalesOrderHeader.CustomerID  = SalesOrderHeader.CustomerID)
WHERE Name = 'Racing Socks, L' AND CompanyName = 'Riding Cycles'


/* Medium questions */

/*
Q6
A "Single Item Order" is a customer order where only one item is ordered. 
Show the SalesOrderID and the UnitPrice for every Single Item Order.
*/

SELECT SalesOrderID, UnitPrice FROM SalesOrderDetail
WHERE (OrderQty = 1)
GROUP BY SalesOrderID, UnitPrice

/*
Q7
Where did the racing socks go? List the product name and the CompanyName 
for all Customers who ordered ProductModel 'Racing Socks'.
*/

SELECT Product.Name, Customer.CompanyName FROM Product
JOIN SalesOrderDetail ON (SalesOrderDetail.ProductID = Product.ProductID)
JOIN SalesOrderHeader ON (SalesOrderHeader.SalesOrderID = SalesOrderDetail.SalesOrderID)
JOIN Customer ON (Customer.CustomerID = SalesOrderHeader.CustomerID)
JOIN ProductModel ON (ProductModel.ProductModelID = Product.ProductModelID)
WHERE (ProductModel.name LIKE 'Racing Socks%')

/*
Q8
Show the product description for culture 'fr' for product with ProductID 736.
*/

SELECT Description FROM ProductDescription 
JOIN ProductModelProductDescription ON (ProductModelProductDescription.ProductDescriptionID = ProductDescription.ProductDescriptionID)
JOIN ProductModel ON (ProductModel.ProductModelID = ProductModelProductDescription.ProductModelID)
JOIN Product ON (Product.ProductModelID = ProductModel.ProductModelID)
WHERE (Product.ProductID = 736 AND Culture = 'fr')

/*
Q9
Use the SubTotal value in SaleOrderHeader to list orders from the largest to the smallest. 
For each order show the CompanyName and the SubTotal and the total weight of the order.
*/

SELECT Subtotal,CompanyName,SUM(OrderQty*Weight) FROM SalesOrderHeader
JOIN Customer ON (Customer.CustomerID = SalesOrderHeader.CustomerID)
JOIN SalesOrderDetail ON (SalesOrderDetail.SalesOrderID = SalesOrderHeader.SalesOrderID)
JOIN Product ON (Product.ProductID = SalesOrderDetail.ProductID)
GROUP BY Subtotal, CompanyName
ORDER BY Subtotal DESC

/*
Q10
How many products in ProductCategory 'Cranksets' have been sold to an address in 'London'?
*/

SELECT COUNT(Product.ProductID) FROM Product 
JOIN ProductCategory ON (ProductCategory.ProductCategoryID = Product.ProductCategoryID)
JOIN SalesOrderDetail ON (SalesOrderDetail.ProductID = Product.ProductID) 
JOIN SalesOrderHeader ON (SalesOrderHeader.SalesOrderID = SalesOrderDetail.SalesOrderID)
JOIN Address ON (Address.AddressID = SalesOrderHeader.ShipToAddressID)
WHERE (Address.City = 'London') AND (ProductCategory.Name = 'Cranksets')
