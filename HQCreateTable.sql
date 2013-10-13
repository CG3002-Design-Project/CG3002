create table Batch (
min_quanity INT,  
selling_price DOUBLE NOT NULL,
quantity INT,
batch_id VARCHAR(256) UNIQUE NOT NULL,
expiry_date DATE,
store_id VARCHAR(256) references Store(store_id),
product_id VARCHAR(256) references Product(product_id),
PRIMARY KEY(store_id,product_id,batch_id)
);

create table Product ( 
product_id VARCHAR(256) PRIMARY KEY,
pricing_strategy VARCHAR(256),
Name VARCHAR(256),
Manufacturer VARCHAR(256)
);

create table product_batch (
cost_price DOUBLE NOT NULL,
batch_id VARCHAR(256) references Batch(batch_id),
product_id VARCHAR(256)  references Product(product_id),
PRIMARY KEY( cost_price, batch_id, product_id)
);


create table Store(
address varchar(256),
region varchar(256), 
store_id varchar(256) UNIQUE NOT NULL, 
Primary key(store_id)
);

create table Employees(
designation varchar(256), 
salary double, 
employee_id varchar(256) UNIQUE NOT NULL,
store_id varchar(256) references Store(store_id),
Primary key(employee_id)
);




create table Transactions(
date_of_transaction  date,
transaction_id varchar(256) UNIQUE NOT NULL,
product_id varchar(256) references Product(product_id),
quantity_sold INT,
store_id VARCHAR(256) references Store(store_id),
cost_price double, 
selling_price double,
Primary key(transaction_id) 
);

