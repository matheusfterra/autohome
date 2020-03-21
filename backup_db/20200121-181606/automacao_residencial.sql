-- MySQL dump 10.13  Distrib 5.7.26, for Win32 (AMD64)
--
-- Host: localhost    Database: automacao_residencial
-- ------------------------------------------------------
-- Server version	5.7.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ar_condicionado`
--

DROP TABLE IF EXISTS `ar_condicionado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ar_condicionado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modelo` varchar(255) NOT NULL,
  `comodo` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ar_condicionado`
--

LOCK TABLES `ar_condicionado` WRITE;
/*!40000 ALTER TABLE `ar_condicionado` DISABLE KEYS */;
/*!40000 ALTER TABLE `ar_condicionado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comodos`
--

DROP TABLE IF EXISTS `comodos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comodos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `iluminacao` tinyint(1) NOT NULL,
  `iluminancia` int(11) NOT NULL,
  `presenca` tinyint(1) NOT NULL,
  `temp_ambiente` int(11) NOT NULL,
  `temp_set` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comodos`
--

LOCK TABLES `comodos` WRITE;
/*!40000 ALTER TABLE `comodos` DISABLE KEYS */;
/*!40000 ALTER TABLE `comodos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicao`
--

DROP TABLE IF EXISTS `medicao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `horario` datetime NOT NULL,
  `corrente` double NOT NULL,
  `tensao` double NOT NULL,
  `potencia` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicao`
--

LOCK TABLES `medicao` WRITE;
/*!40000 ALTER TABLE `medicao` DISABLE KEYS */;
INSERT INTO `medicao` VALUES (1,'2019-12-28 12:26:00',12,221,2652),(2,'2019-12-28 13:00:00',8,219,1752),(3,'2019-12-28 11:30:00',7,220,1540),(4,'2019-12-28 12:00:00',1,1,1),(5,'2019-12-29 15:08:00',3,220,660),(6,'2019-11-29 02:00:00',22,220,4400),(7,'2019-12-29 17:00:00',22,220,2000),(9,'2020-01-13 04:00:00',12,220,2640),(10,'2020-01-13 17:00:00',22,220,4840),(11,'2020-01-13 20:00:00',43,220,7000),(12,'2020-01-13 22:00:00',17,220,4400),(13,'2020-01-13 23:00:00',13,220,1000),(14,'2020-01-13 13:00:00',2,220,550),(15,'2020-01-14 06:00:00',10,220,2200),(16,'2020-01-14 10:00:00',10,220,2200),(17,'2020-01-14 14:00:00',12,220,5390),(18,'2020-01-14 15:00:00',10,220,3421),(19,'2020-01-14 15:00:00',65,220,1000),(20,'2020-01-14 16:00:00',14,220,7532),(21,'2020-01-15 01:00:00',1,1,2222),(22,'2020-01-15 03:00:00',1,1,5555),(23,'2020-01-15 05:00:00',1,220,5000),(24,'2020-01-16 10:00:00',1,220,5000);
/*!40000 ALTER TABLE `medicao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teclas`
--

DROP TABLE IF EXISTS `teclas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teclas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modelo` int(11) NOT NULL,
  `funcao` varchar(255) NOT NULL,
  `codigo` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teclas`
--

LOCK TABLES `teclas` WRITE;
/*!40000 ALTER TABLE `teclas` DISABLE KEYS */;
INSERT INTO `teclas` VALUES (2,2,'teste',22.3);
/*!40000 ALTER TABLE `teclas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-21 18:16:06
