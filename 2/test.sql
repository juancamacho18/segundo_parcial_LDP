create table empleados (id int, nombre string, salario float)
select * from empleados where salario > 2000
update empleados set salario = 3000 where id = 5
delete from empleados where nombre = "Juan"