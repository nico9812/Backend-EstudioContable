INSERT INTO auth_group VALUES(1,'contador');
INSERT INTO auth_group VALUES(2,'cliente');

INSERT INTO documentos_categoria VALUES(1,'Impositivos');
INSERT INTO documentos_categoria VALUES(2,'Seguros');
INSERT INTO documentos_categoria VALUES(3,'Medica');
INSERT INTO documentos_categoria VALUES(4,'Seguro vehicular');
INSERT INTO documentos_categoria VALUES(5,'Programas de higiene y seguridad');
INSERT INTO documentos_categoria VALUES(6,'Otros');

INSERT INTO users_customuser VALUES(1,'pbkdf2_sha256$720000$TAnV84FIT5E2v9pZxsUkmP$CZfa+h6ntMQeHY5ahMSXKNbzaXghbjWEgofcA0gkMl0=','2024-03-15 00:51:28.545680',1,'admin','','',1,1,'2024-03-15 00:51:24.274192',NULL,'',NULL);
INSERT INTO users_customuser VALUES(2,'pbkdf2_sha256$720000$nu3iL5YGdwvF8Br2XuBv7c$1dwt+TDMs/RTR3eZWvXRq0xqOnS60lQA8QN2wcLNkkA=',NULL,0,'contador','','',0,1,'2024-03-15 00:52:00.670579',NULL,'',NULL);
INSERT INTO users_customuser VALUES(3,'pbkdf2_sha256$720000$UGoz9q8z6ffM4V0Gioz7IV$f8UBk4RYJrPzuIY7I6YUwHbXKVumEYQdTrS7DJLNWw4=',NULL,0,'cliente','','',0,1,'2024-03-15 00:52:19.139511',NULL,'',NULL);

INSERT INTO users_customuser_groups VALUES(1,1,2);
INSERT INTO users_customuser_groups VALUES(3,2,1);
INSERT INTO users_customuser_groups VALUES(4,3,2);