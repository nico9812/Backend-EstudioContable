INSERT INTO auth_group VALUES(1,'contador');
INSERT INTO auth_group VALUES(2,'cliente');

INSERT INTO documentos_categoria VALUES(1,'Impositivos');
INSERT INTO documentos_categoria VALUES(2,'Seguros');
INSERT INTO documentos_categoria VALUES(3,'Medica');
INSERT INTO documentos_categoria VALUES(4,'Seguro vehicular');
INSERT INTO documentos_categoria VALUES(5,'Programas de higiene y seguridad');
INSERT INTO documentos_categoria VALUES(6,'Otros');

INSERT INTO users_customuser VALUES(1,'pbkdf2_sha256$720000$jIWuHgZbOCZQCIKDSJaaLY$Chn8MpW/2fW06H8eCI/BLT/9lHpMnaxiA0fGtlPTBrc=','2024-03-11 20:42:53.492520',1,'admin','','',1,1,'2024-03-11 20:42:19.218248',NULL,'',NULL);
INSERT INTO users_customuser VALUES(2,'pbkdf2_sha256$720000$mDKtjXG2SMznlJncQHv4Vk$Jxv1Q8tw2wZYZs3HwQEyRdVLFTfLt6+2JdvTZHAe1iA=',NULL,0,'contador','','',0,1,'2024-03-11 20:43:36.125250',NULL,'',NULL);

INSERT INTO users_customuser_groups VALUES (1, 2, 1);
INSERT INTO users_customuser_groups VALUES (2, 2, 2);