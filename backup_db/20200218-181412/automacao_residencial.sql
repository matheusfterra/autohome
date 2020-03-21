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
-- Table structure for table `configuracao_user`
--

DROP TABLE IF EXISTS `configuracao_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configuracao_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `estado_iluminacao` tinyint(1) NOT NULL,
  `intensidade_iluminacao` int(11) NOT NULL,
  `temperatura` int(11) NOT NULL,
  `aprendizagem` tinyint(1) NOT NULL,
  `economia` tinyint(1) NOT NULL,
  `controle` tinyint(1) NOT NULL,
  `tendencia` int(11) NOT NULL,
  `ar_condicionado` tinyint(1) NOT NULL,
  `televisao` tinyint(1) NOT NULL,
  `temp_banho` int(11) NOT NULL,
  `temp_ar` int(11) NOT NULL,
  `modo_ar` tinyint(1) NOT NULL,
  `volume_tv` int(11) NOT NULL,
  `canais_tv` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuracao_user`
--

LOCK TABLES `configuracao_user` WRITE;
/*!40000 ALTER TABLE `configuracao_user` DISABLE KEYS */;
INSERT INTO `configuracao_user` VALUES (1,1,52,35,1,1,1,60,1,1,36,4,0,3,2);
/*!40000 ALTER TABLE `configuracao_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historico_acoes`
--

DROP TABLE IF EXISTS `historico_acoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historico_acoes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `acao` varchar(255) NOT NULL,
  `valor` varchar(255) NOT NULL,
  `horario` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=72 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_acoes`
--

LOCK TABLES `historico_acoes` WRITE;
/*!40000 ALTER TABLE `historico_acoes` DISABLE KEYS */;
INSERT INTO `historico_acoes` VALUES (37,'Power-Tv','0','2020-01-31 15:45:02'),(36,'Canal-Tv','1','2020-01-31 15:45:00'),(35,'Volume-Tv','1','2020-01-31 15:45:00'),(34,'Power-Tv','1','2020-01-31 15:44:59'),(33,'Power-Ar','0','2020-01-31 15:42:11'),(32,'Temperatura-Ar','1','2020-01-31 15:42:10'),(31,'Temperatura-Ar','1','2020-01-31 15:42:10'),(30,'Modo-Ar','0','2020-01-31 15:42:07'),(29,'Power-Ar','1','2020-01-31 15:42:07'),(28,'Power-Ar','0','2020-01-31 15:40:48'),(27,'Temperatura-Ar','1','2020-01-31 15:40:47'),(26,'Temperatura-Ar','1','2020-01-31 15:40:47'),(25,'Power-Ar','1','2020-01-31 15:40:46'),(24,'Temperatura-Ar','0','2020-01-31 15:40:42'),(23,'Temperatura-Ar','1','2020-01-31 15:34:52'),(22,'Volume-Tv','1','2020-01-31 15:34:51'),(38,'Iluminacao','1','2020-01-31 15:45:58'),(39,'Power-Ar','1','2020-02-02 17:18:10'),(40,'Temperatura-Ar','1','2020-01-21 00:00:00'),(42,'Power-Ar','1','2020-02-07 20:20:06'),(43,'Temperatura-Ar','1','2020-02-07 20:20:07'),(44,'Power-Ar','0','2020-02-07 20:20:09'),(45,'Power-Ar','1','2020-02-07 20:20:42'),(46,'Temperatura-Ar','0','2020-02-07 20:20:43'),(47,'Power-Ar','0','2020-02-07 20:20:44'),(48,'Temperatura-Ar','1','2020-01-21 00:04:00'),(49,'Power-Ar','1','2020-02-08 16:46:43'),(55,'Power-Ar','1','2020-02-08 18:57:33'),(51,'Power-Ar','0','2020-02-08 16:46:47'),(52,'Power-Ar','1','2020-02-08 17:12:21'),(54,'Power-Ar','0','2020-02-08 18:57:30'),(64,'Temperatura-Ar','0','2020-02-07 20:40:43'),(60,'Volume-Tv','1','2020-02-08 19:03:43'),(59,'Power-Tv','1','2020-02-08 19:03:42'),(61,'Canal-Tv','1','2020-02-08 19:03:44'),(62,'Volume-Tv','2','2020-02-08 19:08:14'),(65,'Temperatura-Ar','1','2020-02-09 20:42:09'),(66,'Temperatura-Ar','1','2020-02-09 20:43:00'),(67,'Volume-Tv','1','2020-02-09 19:00:50'),(68,'Canal-Tv','1','2020-02-09 19:00:50'),(69,'Temperatura-Ar','1','2020-01-31 15:35:52'),(70,'Temperatura-Ar','1','2020-01-31 15:36:52');
/*!40000 ALTER TABLE `historico_acoes` ENABLE KEYS */;
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
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicao`
--

LOCK TABLES `medicao` WRITE;
/*!40000 ALTER TABLE `medicao` DISABLE KEYS */;
INSERT INTO `medicao` VALUES (1,'2019-12-28 12:26:00',12,221,2652),(2,'2019-12-28 13:00:00',8,219,1752),(3,'2019-12-28 11:30:00',7,220,1540),(4,'2019-12-28 12:00:00',1,1,1),(5,'2019-12-29 15:08:00',3,220,660),(6,'2019-11-29 02:00:00',22,220,4400),(7,'2019-12-29 17:00:00',22,220,2000),(9,'2020-01-13 04:00:00',12,220,2640),(10,'2020-01-13 17:00:00',22,220,4840),(11,'2020-01-13 20:00:00',43,220,7000),(12,'2020-01-13 22:00:00',17,220,4400),(13,'2020-01-13 23:00:00',13,220,1000),(14,'2020-01-13 13:00:00',2,220,550),(15,'2020-01-14 06:00:00',10,220,2200),(16,'2020-01-14 10:00:00',10,220,2200),(17,'2020-01-14 14:00:00',12,220,5390),(18,'2020-01-14 15:00:00',10,220,3421),(19,'2020-01-14 15:00:00',65,220,1000),(20,'2020-01-14 16:00:00',14,220,7532),(21,'2020-01-15 01:00:00',1,1,2222),(22,'2020-01-15 03:00:00',1,1,5555),(23,'2020-01-15 05:00:00',1,220,5000),(24,'2020-01-16 10:00:00',1,220,5000),(25,'2020-02-01 00:11:00',10,220,2200),(30,'2020-02-02 16:28:00',1,1,5000),(31,'2020-02-03 00:03:00',2,2,1500),(32,'2020-02-07 16:52:00',1,1,3000),(33,'2020-02-08 00:56:00',1,1,4400),(34,'2020-02-09 01:00:00',2,2,500),(35,'2020-02-10 02:00:00',2,2,2000),(36,'2020-02-18 10:17:00',20,220,4400),(37,'2020-02-18 11:00:00',10,220,2200);
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

--
-- Table structure for table `tendencias`
--

DROP TABLE IF EXISTS `tendencias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tendencias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `acao` varchar(255) NOT NULL,
  `horario` datetime NOT NULL,
  `valor` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tendencias`
--

LOCK TABLES `tendencias` WRITE;
/*!40000 ALTER TABLE `tendencias` DISABLE KEYS */;
INSERT INTO `tendencias` VALUES (23,'Temperatura-Ar','1900-01-01 15:49:52',8);
/*!40000 ALTER TABLE `tendencias` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-18 18:14:16
