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
INSERT INTO `configuracao_user` VALUES (1,1,99,34,1,1,1,0,0,35,0,1,55,24);
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
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_acoes`
--

LOCK TABLES `historico_acoes` WRITE;
/*!40000 ALTER TABLE `historico_acoes` DISABLE KEYS */;
INSERT INTO `historico_acoes` VALUES (1,'teste','teste','2010-10-10 12:23:23'),(2,'teste','ligado','2020-01-31 14:58:01'),(3,'teste','ligado','2020-01-31 14:58:46'),(4,'teste','ligado','2020-01-31 14:59:00'),(5,'Ligar-Ar','1','2020-01-31 15:00:35'),(6,'Power-Ar','0','2020-01-31 15:02:40'),(7,'Power-Tv','1','2020-01-31 15:05:41'),(8,'Power-Tv','0','2020-01-31 15:06:04'),(9,'Modo-Ar','0','2020-01-31 15:13:24'),(10,'Modo-Ar','1','2020-01-31 15:13:53'),(11,'Volume','1','2020-01-31 15:18:07'),(12,'Temperatura-Ar','1','2020-01-31 15:19:44'),(13,'Temperatura-Ar','0','2020-01-31 15:19:52');
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

-- Dump completed on 2020-01-31 15:22:42
