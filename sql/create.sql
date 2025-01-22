DROP TABLE shops IF EXISTS;
DROP TABLE positions IF EXISTS;
DROP TABLE workers IF EXISTS;
DROP TABLE cars IF EXISTS;
DROP TABLE dealers IF EXISTS;
DROP TABLE buyers IF EXISTS;
DROP TABLE discount_cards IF EXISTS;
DROP TABLE total_prices IF EXISTS;
DROP TABLE keys_table IF EXISTS;


CREATE TABLE shops
(shopId INTEGER GENERATED ALWAYS AS IDENTITY constraint shop_pk primary key,
name VARCHAR(100) not null,
address VARCHAR(100) not null,
city VARCHAR(100) not null,
rating INTEGER not null
);

CREATE TABLE positions
(position VARCHAR(100) not null,
experience INTEGER not null,
pay INTEGER not null,
PRIMARY KEY (position, experience)
);

CREATE TABLE workers
(workerId INTEGER GENERATED ALWAYS AS IDENTITY constraint worker_pk primary key,
FIO VARCHAR(100) not null,
position VARCHAR(100) not null,
experience INTEGER not null,
skips INTEGER not null,
FOREIGN KEY (position, experience) references positions on update cascade on delete cascade
);

CREATE TABLE cars
(vin INTEGER not null constraint vin_pk primary key,
brand VARCHAR(100) not null,
name VARCHAR(100) not null,
year INTEGER not null,
colour VARCHAR(100) not null,
colourType VARCHAR(100) not null,
body VARCHAR(100) not null,
price INTEGER not null
);

CREATE TABLE dealers
(dealerId INTEGER GENERATED ALWAYS AS IDENTITY constraint dealer_pk primary key,
name VARCHAR(100) not null,
country VARCHAR(100) not null,
region VARCHAR(100) not null,
city VARCHAR(100) not null,
address VARCHAR(100) not null
);

CREATE TABLE buyers
(buyerId INTEGER GENERATED ALWAYS AS IDENTITY constraint buyer_pk primary key,
FIO VARCHAR(100) not null,
phone VARCHAR(100) not null
);

CREATE TABLE discount_cards
(buyerId INTEGER not null constraint buyer_cards_fk references buyers on update cascade on delete cascade,
shopId INTEGER not null constraint shop_cards_fk references shops on update cascade on delete cascade,
type VARCHAR(100) not null
);

CREATE TABLE total_prices
(shopId INTEGER not null constraint shop_tp_fk references shops on update cascade on delete cascade,
vin INTEGER not null constraint vin_tp_fk references cars on update cascade on delete cascade,
buyerId INTEGER not null constraint buyer_tp_fk references buyers on update cascade on delete cascade,
deliveryAddr VARCHAR(100) not null constraint addr_pk primary key,
dealerId INTEGER not null constraint dealer_tp_fk references dealers on update cascade on delete cascade,
totalPrice INTEGER not null
);

CREATE TABLE keys_table
(shopId INTEGER not null constraint shop_kt_fk references shops on update cascade on delete cascade,
workerId INTEGER not null constraint worker_kt_fk references workers on update cascade on delete cascade,
vin INTEGER not null constraint vin_kt_fk references cars on update cascade on delete cascade,
buyerId INTEGER not null constraint buyer_kt_fk references buyers on update cascade on delete cascade,
deliveryAddr VARCHAR(100) not null constraint addr_kt_fk references total_prices on update cascade on delete cascade,
dealerId INTEGER not null constraint dealer_kt_fk references dealers on update cascade on delete cascade
);
