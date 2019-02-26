-- MySQL dump 10.13  Distrib 8.0.12, for Win64 (x86_64)
--
-- Host: localhost    Database: virtual_museum
-- ------------------------------------------------------
-- Server version	8.0.12

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

--
-- Table structure for table `user_info`
--

DROP TABLE IF EXISTS `user_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user_info` (
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL,
  `date_created` date DEFAULT NULL,
  `player_score` int(11) DEFAULT NULL,
  `question_one` varchar(45) NOT NULL,
  `question_two` varchar(45) NOT NULL,
  `question_three` varchar(45) NOT NULL,
  `answer_one` varchar(45) NOT NULL,
  `answer_two` varchar(45) NOT NULL,
  `answer_three` varchar(45) NOT NULL,
  `account_number` int(11) NOT NULL AUTO_INCREMENT,
  `card_number` varchar(19) NOT NULL,
  `exp_date` varchar(5) NOT NULL,
  `cvv` varchar(3) NOT NULL,
  `score` int(255) DEFAULT NULL,
  PRIMARY KEY (`account_number`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `account_number_UNIQUE` (`account_number`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_info`
--

LOCK TABLES `user_info` WRITE;
/*!40000 ALTER TABLE `user_info` DISABLE KEYS */;
INSERT INTO `user_info` VALUES ('Kevin','Montero','kevinwilding1997@gmail.com','$5$rounds=535000$csqzjTKaUxHxUeGp$nQchJPIHdZV.agFCoYR4sMVS.STRKYQV/a.aVP266WC','2019-02-22',NULL,'48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&',1,'1234 1234 1234 1234','12/12','123',NULL),('Manuel','Gonzales','mg@example.com','$5$rounds=535000$uTJctDgwSTNIFC.P$0EAtVlyTpDFHESaDtbRTtLgmAVFeVdJUS03TElqZoo8','2019-02-22',NULL,'48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&',2,'1234 1234 1234 1234','12/12','123',NULL),('Moises ','Montero','moises@gmail.com','$5$rounds=535000$Zg.Z1KIYx6PYjCSK$dwqGnhsFZqFbDKR2xyUnkIitG3PquRzSeLjHgOxR1IC','2019-02-22',NULL,'48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&',3,'1234 1234 1234 1234','12/12','123',NULL),('Abigail','Montero','Abi@example.com','$5$rounds=535000$7RlWmcsl/IhOyFIC$QCu.2Kfg0lvLlZbHzR/fdajYfe7OeOxilicDjWLzUE5','2019-02-23',NULL,'48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&',4,'1234 1234 1234 1234','12/12','123',NULL),('Moises','Montero','moisesmontero@gmail.com','$5$rounds=535000$xRJ9S6n1//nSE3CX$OXAyGa82h0mEVsnUTWUV02JTaE/HpEtr0Bz2qAL.Fs6','2019-02-25',NULL,'48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&',5,'0000 0000 0000 0000','12/12','123',NULL),('Moises','Montero','mmontero2003@gmail.com','$5$rounds=535000$Kxj2hlCcGsqs1GtK$1pcAA5EESGR7jSafrerzTrIn5zIftcjQfcXZEjLhFK5','2019-02-25',NULL,'48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&',7,'0000 0000 0000 0000','12/12','123',NULL),('Moises','Montero','mmontero2009@gmail.com','$5$rounds=535000$RL6S6T107i1sTZNv$qkDKaUkxj2nHCE0EN99.Rm13ArvQYIOYBZQZuqZW97B','2019-02-25',NULL,'48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&','48$%*($*#&',9,'0000 0000 0000 0000','12/12','123',NULL);
/*!40000 ALTER TABLE `user_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-25 17:54:57
