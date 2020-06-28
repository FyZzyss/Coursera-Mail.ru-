use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product

-- 2. Выбрать названия всех автоматизированных складов
select name from store where is_automated = 1

-- 3. Посчитать общую сумму в деньгах всех продаж
SELECT SUM(total) from sale

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
SELECT store_id from store natural left join sale where sale_id is not null group by store_id

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
SELECT store_id from store natural left join sale where sale_id is null group by store_id

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
SELECT name, avg(total / quantity) from sale natural join product group by name

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select any_value(name) from product natural join sale group by store_id having count(distinct name)=1

-- 8. Получить названия всех складов, с которых продавался только один продукт
select any_value(name) from store natural join sale group by product_id having count(distinct name)=1

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale order by total desc limit 1

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
SELECT date from product natural join sale group by date order by sum(total) desc, date limit 1
