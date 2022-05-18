/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

/* CREATE DATABASE IF NOT EXISTS `portal_paciente_LR`;*/

/* GRANT ALL ON `portal_paciente_LR`.* TO 'root'@'%';*/

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` (`id`, `name`) VALUES (1,'DIABÉTICO');
INSERT INTO `category` (`id`, `name`) VALUES (2,'HIPERTENSO');
INSERT INTO `category` (`id`, `name`) VALUES (3,'ENFERMEDAD RESPIRATORIA CRÓNICA');
INSERT INTO `category` (`id`, `name`) VALUES (4,'ENFERMEDAD RENAL CRÓNICA');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `gender`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `gender` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gender`
--

LOCK TABLES `gender` WRITE;
/*!40000 ALTER TABLE `gender` DISABLE KEYS */;
INSERT INTO `gender` (`id`, `name`) VALUES (1,'MASCULINO');
INSERT INTO `gender` (`id`, `name`) VALUES (2,'FEMENINO');
INSERT INTO `gender` (`id`, `name`) VALUES (3,'NO BINARIO');
/*!40000 ALTER TABLE `gender` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `person_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `person_status` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_status`
--

LOCK TABLES `person_status` WRITE;
/*!40000 ALTER TABLE `person_status` DISABLE KEYS */;
INSERT INTO `person_status` (`id`, `name`) VALUES (1,'EMAIL PENDIENTE DE VALIDACIÓN');
INSERT INTO `person_status` (`id`, `name`) VALUES (2,'EMAIL VALIDADO');
INSERT INTO `person_status` (`id`, `name`) VALUES (3,'EMAIL RECHAZADO');
/*!40000 ALTER TABLE `person_status` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `admin_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `admin_status` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_status`
--

LOCK TABLES `admin_status` WRITE;
/*!40000 ALTER TABLE `admin_status` DISABLE KEYS */;
INSERT INTO `admin_status` (`id`, `name`) VALUES (1,'PENDIENTE DE VALIDACIÓN');
INSERT INTO `admin_status` (`id`, `name`) VALUES (2,'VALIDADO');
INSERT INTO `admin_status` (`id`, `name`) VALUES (3,'RECHAZADO');
/*!40000 ALTER TABLE `admin_status` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Table structure for table `expiration_black_list`
--

DROP TABLE IF EXISTS `expiration_black_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `expiration_black_list` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `register_datetime` datetime DEFAULT NULL,
  `token` varchar(500) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expiration_black_list`
--

LOCK TABLES `expiration_black_list` WRITE;
/*!40000 ALTER TABLE `expiration_black_list` DISABLE KEYS */;
INSERT INTO `expiration_black_list` (`id`, `register_datetime`, `token`) VALUES (1,'2022-01-31 16:05:06','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0MzcwMjY4Mn0.3p6CHbRhwnPyMRlkXLPiQlSpSdLbAeW36fvK1P8EM1M');
INSERT INTO `expiration_black_list` (`id`, `register_datetime`, `token`) VALUES (2,'2022-01-31 16:05:30','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0MzcwMjY4Mn0.3p6CHbRhwnPyMRlkXLPiQlSpSdLbAeW36fvK1P8EM1M');
INSERT INTO `expiration_black_list` (`id`, `register_datetime`, `token`) VALUES (3,'2022-02-01 15:43:02','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0Mzc0MDg5OX0.THK6m1gH8q2hoBEgbFfvos0RWYbPVQ81KM4qgnKd4H4');
INSERT INTO `expiration_black_list` (`id`, `register_datetime`, `token`) VALUES (4,'2022-02-01 17:16:11','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0Mzc0MDg5OX0.THK6m1gH8q2hoBEgbFfvos0RWYbPVQ81KM4qgnKd4H4');
INSERT INTO `expiration_black_list` (`id`, `register_datetime`, `token`) VALUES (5,'2022-02-08 01:34:24','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0NDI5MjE1NH0.zGlsMyKRifRYGVVRTvmBKJT0T2L6EC2aRtkdGSVfnjw');
INSERT INTO `expiration_black_list` (`id`, `register_datetime`, `token`) VALUES (6,'2022-02-08 16:04:57','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0NDM0NjU4NX0.LsLWDXXXJSFetdKbqQCvRyGed7sSPYRRlGnXLYf1IjQ');
INSERT INTO `expiration_black_list` (`id`, `register_datetime`, `token`) VALUES (7,'2022-02-08 17:06:29','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0NDM1MDcxNH0.2yR43luQkzgE_uM4imlZDmNZBWvtEqj8zugYYRarjV4');
INSERT INTO `expiration_black_list` (`id`, `register_datetime`, `token`) VALUES (8,'2022-02-08 17:15:05','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0NDM1MDcxNH0.2yR43luQkzgE_uM4imlZDmNZBWvtEqj8zugYYRarjV4');
/*!40000 ALTER TABLE `expiration_black_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `identification_type`
--

DROP TABLE IF EXISTS `identification_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `identification_type` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `identification_type`
--

LOCK TABLES `identification_type` WRITE;
/*!40000 ALTER TABLE `identification_type` DISABLE KEYS */;
INSERT INTO `identification_type` (`id`, `name`) VALUES (1,'DNI');
/*!40000 ALTER TABLE `identification_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `message` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `register_datetime` datetime DEFAULT NULL,
  `header` varchar(500) COLLATE latin1_spanish_ci DEFAULT NULL,
  `body` varchar(4000) COLLATE latin1_spanish_ci DEFAULT NULL,
  `is_formatted` tinyint DEFAULT 0,
  `sent_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` (`id`, `register_datetime`, `header`, `body`) VALUES (1,'2022-02-07 07:25:00','Título del primer mensaje','Cuerpo del primer mensaje.');
INSERT INTO `message` (`id`, `register_datetime`, `header`, `body`) VALUES (2,'2022-02-08 10:29:00','Título del segundo mensaje','Cuerpo del segundo mensaje.');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `permission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `url` varchar(1000) COLLATE latin1_spanish_ci DEFAULT NULL,
  `method` varchar(10) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (1,'Get Identification Types','/portalpaciente/api/v1/parametric/identificationtypes','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (2,'Get Provinces','/portalpaciente/api/v1/parametric/provinces','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (3,'Get Allergies','/portalpaciente/api/v1/hcegeneral/.*/allergies/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (4,'Get Anthropometric Data','/portalpaciente/api/v1/hcegeneral/.*/anthropometricData/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (5,'Get Chronic','/portalpaciente/api/v1/hcegeneral/.*/chronic/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (6,'Get Family Histories','/portalpaciente/api/v1/hcegeneral/.*/familyHistories/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (7,'Get Hospitalization','/portalpaciente/api/v1/hcegeneral/.*/hospitalization/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (8,'Get Immunizations','/portalpaciente/api/v1/hcegeneral/.*/immunizations/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (9,'Get Medications','/portalpaciente/api/v1/hcegeneral/.*/medications/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (10,'Get Personal Histories','/portalpaciente/api/v1/hcegeneral/.*/personalHistories/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (11,'Get Tooth Records','/portalpaciente/api/v1/hcegeneral/.*/toothRecords/.*/tooth/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (12,'Get Active Problems','/portalpaciente/api/v1/hcegeneral/.*/activeProblems/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (13,'Get Solved Problems','/portalpaciente/api/v1/hcegeneral/.*/solvedProblems/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (14,'Get Vital Signs','/portalpaciente/api/v1/hcegeneral/.*/vitalSigns/.*','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (15,'All Institutions','/portalpaciente/api/v1/institutions/all','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (16,'Basic Data','/portalpaciente/api/v1/patient/basicData','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (17,'Complete Data','/portalpaciente/api/v1/patient/completeData','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (18,'Create User','/portalpaciente/api/v1/createuser','POST');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (19,'Get Messages','/portalpaciente/api/v1/getmessages','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (20,'Set Messages Read','/portalpaciente/api/v1/setmessagesread','POST');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (21,'Create Person','/portalpaciente/api/v1/createperson','POST');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (22,'Update Person','/portalpaciente/api/v1/updateperson','PUT');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (23,'Delete Person','/portalpaciente/api/v1/deleteperson','PUT');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (24,'Get Person by id','/portalpaciente/api/v1/getpersonbyid','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (25,'Get Person by identification number','/portalpaciente/api/v1/getpersonbyidentificationnumber','GET');
INSERT INTO `permission` (`id`, `name`, `url`, `method`) VALUES (26,'Set Admin status to Person','/portalpaciente/api/v1/setadminstatustoperson','PUT');



/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `person` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `surname` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `identification_number` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `id_gender` bigint(20) DEFAULT NULL,
  `id_department` bigint(20) DEFAULT NULL,
  `id_locality` bigint(20) DEFAULT NULL,
  `address_street` varchar(250) COLLATE latin1_spanish_ci DEFAULT NULL,
  `address_number` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `id_usual_institution` bigint(20) DEFAULT NULL,
  `is_diabetic` tinyint DEFAULT NULL,
  `is_hypertensive` tinyint DEFAULT NULL,
  `is_chronic_respiratory_disease` tinyint DEFAULT NULL,
  `is_chronic_kidney_disease` tinyint DEFAULT NULL,
  `identification_number_master` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `id_identification_type` bigint(20) DEFAULT NULL,
  `id_identification_type_master` bigint(20) DEFAULT NULL,
  `is_deleted` tinyint DEFAULT NULL,
  `id_patient` bigint(20) DEFAULT NULL,
  `id_admin_status` tinyint DEFAULT NULL,
  `phone_number` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  `department` varchar(200) COLLATE latin1_spanish_ci DEFAULT NULL,
  `locality` varchar(200) COLLATE latin1_spanish_ci DEFAULT NULL,
  `email` varchar(200) COLLATE latin1_spanish_ci DEFAULT NULL,
  `identification_front_image` longtext COLLATE latin1_spanish_ci,
  `identification_back_image` longtext COLLATE latin1_spanish_ci,
  `identification_front_image_file_type` varchar(45) COLLATE latin1_spanish_ci,
  `identification_back_image_file_type` varchar(45) COLLATE latin1_spanish_ci,
  `id_person_status` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` (`id`, `name`, `surname`, `birthdate`, `identification_number`) VALUES (1,'Administrador','Administrador','1970-01-01','1054201');
INSERT INTO `person` (`id`, `name`, `surname`, `birthdate`, `identification_number`) VALUES (2,'Emmanuel','Arias','1990-01-01','31045285');
INSERT INTO `person` (`id`, `name`, `surname`, `birthdate`, `identification_number`) VALUES (3,'Osvaldo','Ocanto','1979-01-01','27543642');
INSERT INTO `person` (`id`, `name`, `surname`, `birthdate`, `identification_number`) VALUES (4,'Ernesto','Sábato','1950-01-01','4545609');
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` (`id`, `name`) VALUES (1,'Administrativo');
INSERT INTO `role` (`id`, `name`) VALUES (2,'Médico');
INSERT INTO `role` (`id`, `name`) VALUES (3,'Auxiliar');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permission`
--

DROP TABLE IF EXISTS `role_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `role_permission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_permission` bigint(20) DEFAULT NULL,
  `id_role` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permission`
--

LOCK TABLES `role_permission` WRITE;
/*!40000 ALTER TABLE `role_permission` DISABLE KEYS */;
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (1,1,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (2,2,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (3,3,2);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (4,4,2);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (5,5,3);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (6,6,3);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (7,19,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (8,19,2);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (9,19,3);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (10,20,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (11,20,2);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (12,20,3);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (13,7,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (14,8,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (15,9,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (16,10,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (17,11,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (18,12,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (19,13,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (20,14,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (21,15,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (22,16,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (23,17,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (24,18,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (25,21,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (26,22,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (27,23,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (28,24,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (29,25,1);
INSERT INTO `role_permission` (`id`, `id_permission`, `id_role`) VALUES (30,26,1);
/*!40000 ALTER TABLE `role_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) COLLATE latin1_spanish_ci NULL,
  `password` varchar(500) COLLATE latin1_spanish_ci NULL DEFAULT '',
  `id_person` bigint(20) NULL,
  `id_user_status` bigint(20) NULL,
  `is_admin` bigint(20) NULL DEFAULT 0,
  `is_mail_validate` bigint(20) NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `username`, `password`, `id_person`, `id_user_status`) VALUES (1,'admin','$2b$12$nW9bzZJggFAyYYI.soU8GurU.0g82ftRBNfn.v9vtIDWmt/RJdgr2',1,1);
INSERT INTO `user` (`id`, `username`, `password`, `id_person`, `id_user_status`) VALUES (2,'earias','$2b$12$nW9bzZJggFAyYYI.soU8GurU.0g82ftRBNfn.v9vtIDWmt/RJdgr2',2,1);
INSERT INTO `user` (`id`, `username`, `password`, `id_person`, `id_user_status`) VALUES (3,'oocanto','$2b$12$nW9bzZJggFAyYYI.soU8GurU.0g82ftRBNfn.v9vtIDWmt/RJdgr2',3,1);
INSERT INTO `user` (`id`, `username`, `password`, `id_person`, `id_user_status`) VALUES (4,'esabato','$2b$12$nW9bzZJggFAyYYI.soU8GurU.0g82ftRBNfn.v9vtIDWmt/RJdgr2',4,1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_category`
--

DROP TABLE IF EXISTS `user_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user_category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_user` bigint(20) DEFAULT NULL,
  `id_category` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_category`
--

LOCK TABLES `user_category` WRITE;
/*!40000 ALTER TABLE `user_category` DISABLE KEYS */;
INSERT INTO `user_category` (`id`, `id_user`, `id_category`) VALUES (1,1,1);
INSERT INTO `user_category` (`id`, `id_user`, `id_category`) VALUES (2,2,2);
INSERT INTO `user_category` (`id`, `id_user`, `id_category`) VALUES (3,3,1);
INSERT INTO `user_category` (`id`, `id_user`, `id_category`) VALUES (4,4,2);
/*!40000 ALTER TABLE `user_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person_message`
--

DROP TABLE IF EXISTS `person_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `person_message` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_person` bigint(20) DEFAULT NULL,
  `id_message` bigint(20) DEFAULT NULL,
  `read_datetime` varchar(45) COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_message`
--

LOCK TABLES `person_message` WRITE;
/*!40000 ALTER TABLE `person_message` DISABLE KEYS */;
INSERT INTO `person_message` (`id`, `id_person`, `id_message`, `read_datetime`) VALUES (1,1,1,'2022-02-08 15:15:59.556278');
INSERT INTO `person_message` (`id`, `id_person`, `id_message`, `read_datetime`) VALUES (2,2,1,NULL);
INSERT INTO `person_message` (`id`, `id_person`, `id_message`, `read_datetime`) VALUES (3,3,2,NULL);
INSERT INTO `person_message` (`id`, `id_person`, `id_message`, `read_datetime`) VALUES (4,4,2,NULL);
INSERT INTO `person_message` (`id`, `id_person`, `id_message`, `read_datetime`) VALUES (5,1,2,NULL);
/*!40000 ALTER TABLE `person_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_role`
--

DROP TABLE IF EXISTS `user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_role` bigint(20) DEFAULT NULL,
  `id_user` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role`
--

LOCK TABLES `user_role` WRITE;
/*!40000 ALTER TABLE `user_role` DISABLE KEYS */;
INSERT INTO `user_role` (`id`, `id_role`, `id_user`) VALUES (1,1,1);
INSERT INTO `user_role` (`id`, `id_role`, `id_user`) VALUES (2,1,2);
INSERT INTO `user_role` (`id`, `id_role`, `id_user`) VALUES (3,2,3);
INSERT INTO `user_role` (`id`, `id_role`, `id_user`) VALUES (4,3,4);
/*!40000 ALTER TABLE `user_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_status`
--

DROP TABLE IF EXISTS `user_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user_status` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_status`
--

LOCK TABLES `user_status` WRITE;
/*!40000 ALTER TABLE `user_status` DISABLE KEYS */;
INSERT INTO `user_status` (`id`, `name`) VALUES (1,'Activo');
INSERT INTO `user_status` (`id`, `name`) VALUES (2,'Inactivo');
/*!40000 ALTER TABLE `user_status` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-08 17:20:47
