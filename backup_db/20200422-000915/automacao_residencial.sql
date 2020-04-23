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
  `COM` varchar(55) NOT NULL,
  `date_agrupamento_medicoes` timestamp NOT NULL,
  `agrupamento_medicoes` tinyint(1) NOT NULL,
  `date_backup` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuracao_user`
--

LOCK TABLES `configuracao_user` WRITE;
/*!40000 ALTER TABLE `configuracao_user` DISABLE KEYS */;
INSERT INTO `configuracao_user` VALUES (1,0,99,31,1,1,1,24,0,0,22,24,0,5,3,'COM8','2020-04-22 03:07:15',0,'2020-04-17 21:54:22');
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
) ENGINE=MyISAM AUTO_INCREMENT=405 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_acoes`
--

LOCK TABLES `historico_acoes` WRITE;
/*!40000 ALTER TABLE `historico_acoes` DISABLE KEYS */;
INSERT INTO `historico_acoes` VALUES (37,'Power-Tv','0','2020-01-31 15:45:02'),(36,'Canal-Tv','1','2020-01-31 15:45:00'),(35,'Volume-Tv','1','2020-01-31 15:45:00'),(34,'Power-Tv','1','2020-01-31 15:44:59'),(33,'Power-Ar-Off','0','2020-01-31 15:42:11'),(32,'Temperatura-Ar-Mais','1','2020-01-31 15:42:10'),(31,'Temperatura-Ar-Mais','1','2020-01-31 15:42:10'),(30,'Modo-Ar','0','2020-01-31 15:42:07'),(29,'Power-Ar-On','1','2020-01-31 15:42:07'),(28,'Power-Ar-Off','0','2020-01-31 15:40:48'),(27,'Temperatura-Ar-Mais','1','2020-01-31 15:40:47'),(26,'Temperatura-Ar-Mais','1','2020-01-31 15:40:47'),(25,'Power-Ar-On','1','2020-01-31 15:40:46'),(24,'Temperatura-Ar-Menos','1','2020-01-31 15:40:42'),(23,'Temperatura-Ar-Mais','1','2020-01-31 15:34:52'),(22,'Volume-Tv','1','2020-01-31 15:34:51'),(38,'Iluminacao','1','2020-01-31 15:45:58'),(39,'Power-Ar-On','1','2020-02-02 17:18:10'),(40,'Temperatura-Ar-Mais','1','2020-01-21 00:00:00'),(42,'Power-Ar-On','1','2020-02-07 20:20:06'),(43,'Temperatura-Ar-Mais','1','2020-02-07 20:20:07'),(44,'Power-Ar-Off','0','2020-02-07 20:20:09'),(45,'Power-Ar-On','1','2020-02-07 20:20:42'),(46,'Temperatura-Ar-Menos','1','2020-02-07 20:20:43'),(47,'Power-Ar-Off','0','2020-02-07 20:20:44'),(48,'Temperatura-Ar-Mais','1','2020-01-21 00:04:00'),(49,'Power-Ar-On','1','2020-02-08 16:46:43'),(55,'Power-Ar-On','1','2020-02-08 18:57:33'),(51,'Power-Ar-Off','0','2020-02-08 16:46:47'),(52,'Power-Ar-On','1','2020-02-08 17:12:21'),(54,'Power-Ar-On','0','2020-02-08 18:57:30'),(64,'Temperatura-Ar-Menos','1','2020-02-07 20:40:43'),(60,'Volume-Tv','1','2020-02-08 19:03:43'),(59,'Power-Tv','1','2020-02-08 19:03:42'),(61,'Canal-Tv','1','2020-02-08 19:03:44'),(62,'Volume-Tv','2','2020-02-08 19:08:14'),(65,'Temperatura-Ar-Mais','1','2020-02-09 20:42:09'),(66,'Temperatura-Ar-Mais','1','2020-02-09 20:43:00'),(67,'Volume-Tv','1','2020-02-09 19:00:50'),(68,'Canal-Tv','1','2020-02-09 19:00:50'),(69,'Temperatura-Ar-Mais','1','2020-01-31 15:35:52'),(70,'Temperatura-Ar-Mais','1','2020-01-31 15:36:52'),(72,'Power-Ar-Off','0','2020-02-18 18:16:03'),(73,'Temperatura-Ar-Mais','1','2020-02-20 15:36:52'),(95,'Temperatura-Ar-Mais','1','2020-01-31 00:05:10'),(92,'Temperatura-Ar-Menos','1','2020-02-14 20:57:00'),(88,'Temperatura-Ar-Menos','1','2020-02-07 20:43:43'),(89,'Temperatura-Ar-Menos','1','2020-02-07 20:39:43'),(90,'Temperatura-Ar-Menos','1','2020-02-07 20:54:42'),(103,'Power-Ar-On','1','2020-03-04 08:59:48'),(102,'Power-Ar-Off','0','2020-03-03 11:46:13'),(104,'Temperatura-Ar-Mais','1','2020-03-04 08:59:49'),(105,'Temperatura-Ar-Mais','1','2020-03-04 09:00:20'),(106,'Temperatura-Ar-Mais','1','2020-03-04 09:00:32'),(107,'Temperatura-Ar-Mais','1','2020-03-04 09:00:33'),(108,'Temperatura-Ar-Mais','1','2020-03-04 09:00:33'),(109,'Temperatura-Ar-Mais','1','2020-03-04 09:00:33'),(110,'Temperatura-Ar-Mais','1','2020-03-04 09:00:33'),(111,'Temperatura-Ar-Mais','1','2020-03-04 09:00:33'),(112,'Temperatura-Ar-Mais','1','2020-03-04 09:00:33'),(113,'Temperatura-Ar-Mais','1','2020-03-04 09:00:33'),(114,'Temperatura-Ar-Mais','1','2020-03-04 09:00:34'),(115,'Temperatura-Ar-Mais','1','2020-03-04 09:00:34'),(116,'Temperatura-Ar-Mais','1','2020-03-04 09:00:34'),(117,'Temperatura-Ar-Mais','1','2020-03-04 09:00:34'),(118,'Temperatura-Ar-Mais','1','2020-03-04 09:00:34'),(119,'Iluminacao','1','2020-03-23 12:28:28'),(120,'Iluminacao','0','2020-03-23 12:28:32'),(121,'Iluminacao','1','2020-03-23 12:28:35'),(122,'Iluminacao','0','2020-03-23 12:28:37'),(123,'Iluminacao','1','2020-03-23 12:29:03'),(124,'Iluminacao','0','2020-03-23 12:29:07'),(125,'Iluminacao','1','2020-03-23 12:29:08'),(126,'Iluminacao','0','2020-03-23 12:29:10'),(127,'Iluminacao','1','2020-03-23 12:29:13'),(128,'Iluminacao','0','2020-03-23 12:29:14'),(129,'Iluminacao','1','2020-03-23 12:29:16'),(130,'Iluminacao','0','2020-03-23 12:29:18'),(131,'Iluminacao','1','2020-03-23 12:29:32'),(132,'Iluminacao','0','2020-03-23 12:29:33'),(133,'Iluminacao','1','2020-03-23 12:29:35'),(134,'Iluminacao','0','2020-03-23 12:29:39'),(135,'Iluminacao','1','2020-03-23 12:49:18'),(136,'Iluminacao','0','2020-03-23 12:49:21'),(137,'Iluminacao','1','2020-03-23 12:49:23'),(138,'Iluminacao','0','2020-03-23 12:49:25'),(139,'Iluminacao','1','2020-03-23 12:49:31'),(140,'Iluminacao','0','2020-03-23 12:49:37'),(141,'Iluminacao','1','2020-03-23 12:50:08'),(142,'Iluminacao','0','2020-03-23 12:50:09'),(143,'Iluminacao','1','2020-03-23 12:50:11'),(144,'Iluminacao','0','2020-03-23 12:50:14'),(145,'Iluminacao','1','2020-03-23 16:49:09'),(146,'Iluminacao','1','2020-03-23 16:53:51'),(147,'Iluminacao','1','2020-03-23 16:57:59'),(148,'Iluminacao','0','2020-03-23 16:58:02'),(149,'Iluminacao','1','2020-03-23 16:58:13'),(150,'Iluminacao','0','2020-03-23 16:58:17'),(151,'Iluminacao','1','2020-03-23 16:59:06'),(152,'Iluminacao','0','2020-03-23 16:59:09'),(153,'Iluminacao','1','2020-03-23 17:01:00'),(154,'Iluminacao','0','2020-03-23 17:01:44'),(155,'Iluminacao','1','2020-03-23 17:02:53'),(156,'Iluminacao','0','2020-03-23 17:03:08'),(157,'Iluminacao','1','2020-03-23 17:14:57'),(158,'Iluminacao','0','2020-03-23 17:15:03'),(159,'Iluminacao','1','2020-03-23 17:15:05'),(160,'Iluminacao','0','2020-03-23 17:15:08'),(161,'Iluminacao','1','2020-03-24 11:14:39'),(162,'Iluminacao','0','2020-03-24 11:14:42'),(163,'Power-Ar-Off','0','2020-03-25 12:29:31'),(164,'Power-Ar-On','1','2020-03-25 12:29:37'),(165,'Power-Ar-Off','0','2020-03-25 12:30:15'),(166,'Power-Ar-On','1','2020-03-25 12:30:17'),(167,'Power-Ar-Off','0','2020-04-06 15:37:35'),(168,'Power-Ar-On','1','2020-04-06 15:37:40'),(169,'Power-Ar-Off','0','2020-04-06 15:37:41'),(170,'Power-Ar-On','1','2020-04-06 15:37:44'),(171,'Power-Ar-Off','0','2020-04-06 15:37:46'),(172,'Power-Ar-On','1','2020-04-06 15:37:49'),(173,'Power-Ar-Off','0','2020-04-06 15:38:04'),(174,'Power-Ar-On','1','2020-04-06 15:49:12'),(175,'Power-Ar-Off','0','2020-04-06 15:49:20'),(176,'Power-Ar-On','1','2020-04-06 15:49:28'),(177,'Temperatura-Ar-Mais','1','2020-04-06 16:08:46'),(178,'Temperatura-Ar-Mais','1','2020-04-06 16:09:19'),(179,'Temperatura-Ar-Mais','1','2020-04-06 16:09:30'),(180,'Power-Ar-Off','0','2020-04-06 16:11:01'),(181,'Power-Ar-On','1','2020-04-06 16:11:44'),(182,'Power-Ar-Off','0','2020-04-06 16:11:46'),(183,'Power-Ar-On','1','2020-04-06 16:11:47'),(184,'Power-Ar-Off','0','2020-04-06 16:11:48'),(185,'Power-Ar-On','1','2020-04-06 16:11:48'),(186,'Power-Ar-Off','0','2020-04-06 16:11:52'),(187,'Power-Ar-On','1','2020-04-06 16:11:53'),(188,'Power-Ar-Off','0','2020-04-06 16:12:42'),(189,'Power-Ar-On','1','2020-04-06 16:14:49'),(190,'Power-Ar-Off','0','2020-04-06 16:14:52'),(191,'Power-Ar-On','1','2020-04-06 16:14:58'),(192,'Power-Ar-Off','0','2020-04-06 16:15:03'),(193,'Power-Ar-On','1','2020-04-06 16:15:15'),(194,'Temperatura-Ar-Mais','1','2020-04-06 16:15:19'),(195,'Temperatura-Ar-Menos','0','2020-04-06 16:19:18'),(196,'Temperatura-Ar-Menos','0','2020-04-06 16:19:20'),(197,'Temperatura-Ar-Menos','0','2020-04-06 16:19:22'),(198,'Temperatura-Ar-Menos','0','2020-04-06 16:19:24'),(199,'Temperatura-Ar-Menos','0','2020-04-06 16:19:26'),(200,'Temperatura-Ar-Mais','1','2020-04-06 16:19:57'),(201,'Temperatura-Ar-Mais','1','2020-04-06 16:19:57'),(202,'Temperatura-Ar-Mais','1','2020-04-06 16:19:59'),(203,'Temperatura-Ar-Mais','1','2020-04-06 16:20:00'),(204,'Temperatura-Ar-Mais','1','2020-04-06 16:20:01'),(205,'Temperatura-Ar-Mais','1','2020-04-06 16:20:02'),(206,'Temperatura-Ar-Mais','1','2020-04-06 16:20:03'),(207,'Temperatura-Ar-Menos','0','2020-04-06 16:20:27'),(208,'Temperatura-Ar-Menos','0','2020-04-06 16:20:28'),(209,'Temperatura-Ar-Menos','0','2020-04-06 16:20:29'),(210,'Temperatura-Ar-Menos','0','2020-04-06 16:20:30'),(211,'Temperatura-Ar-Menos','0','2020-04-06 16:20:31'),(212,'Temperatura-Ar-Menos','0','2020-04-06 16:20:31'),(213,'Temperatura-Ar-Menos','0','2020-04-06 16:20:33'),(214,'Temperatura-Ar-Menos','0','2020-04-06 16:20:34'),(215,'Modo-Ar','1','2020-04-06 16:26:12'),(216,'Modo-Ar','0','2020-04-06 16:26:17'),(217,'Power-Ar-Off','0','2020-04-06 16:26:46'),(218,'Power-Ar-On','1','2020-04-06 16:34:32'),(219,'Temperatura-Ar-Mais','1','2020-04-06 16:34:38'),(220,'Temperatura-Ar-Menos','0','2020-04-06 16:34:42'),(221,'Modo-Ar','1','2020-04-06 16:34:45'),(222,'Modo-Ar','0','2020-04-06 16:34:47'),(223,'Power-Ar-Off','0','2020-04-06 16:34:50'),(224,'Volume-Tv','1','2020-04-06 16:34:57'),(225,'Volume-Tv','0','2020-04-06 16:35:01'),(226,'Canal-Tv','1','2020-04-06 16:35:04'),(227,'Canal-Tv','0','2020-04-06 16:35:07'),(228,'Power-Tv','1','2020-04-06 16:36:39'),(229,'Power-Tv','0','2020-04-06 16:36:40'),(230,'Power-Ar-On','1','2020-04-06 16:41:55'),(231,'Power-Ar-Off','0','2020-04-06 16:42:03'),(232,'Power-Ar-On','1','2020-04-06 16:43:29'),(233,'Power-Ar-Off','0','2020-04-06 16:43:42'),(234,'Power-Ar-On','1','2020-04-06 17:29:19'),(235,'Temperatura-Ar-Mais','1','2020-04-06 17:35:54'),(236,'Power-Ar-Off','0','2020-04-06 17:36:17'),(237,'Power-Ar-On','1','2020-04-06 17:36:20'),(238,'Power-Tv','1','2020-04-07 18:34:38'),(239,'Volume-Tv','1','2020-04-07 18:34:41'),(240,'Volume-Tv','0','2020-04-07 18:34:44'),(241,'Canal-Tv','1','2020-04-07 18:34:47'),(242,'Canal-Tv','0','2020-04-07 18:34:50'),(243,'Power-Tv','0','2020-04-07 18:34:53'),(244,'Power-Tv','1','2020-04-07 19:56:48'),(245,'Power-Tv','0','2020-04-07 19:57:08'),(246,'Power-Tv','1','2020-04-07 20:00:15'),(247,'Power-Tv','0','2020-04-07 20:00:28'),(248,'Power-Tv','1','2020-04-07 20:04:13'),(249,'Power-Tv','0','2020-04-07 20:04:54'),(250,'Power-Tv','1','2020-04-07 20:07:04'),(251,'Power-Tv','0','2020-04-07 20:08:01'),(252,'Power-Tv','1','2020-04-07 20:08:48'),(253,'Power-Tv','0','2020-04-07 20:10:38'),(254,'Power-Tv','1','2020-04-07 20:13:45'),(255,'Power-Tv','0','2020-04-08 12:33:20'),(256,'Power-Tv','1','2020-04-08 12:35:16'),(257,'Power-Tv','0','2020-04-08 12:41:48'),(258,'Power-Tv','1','2020-04-08 12:42:34'),(259,'Power-Tv','0','2020-04-08 12:42:47'),(260,'Power-Tv','1','2020-04-08 12:43:16'),(261,'Power-Tv','0','2020-04-08 12:43:22'),(262,'Power-Tv','1','2020-04-08 12:46:54'),(263,'Power-Tv','0','2020-04-08 13:46:27'),(264,'Power-Tv','1','2020-04-08 13:46:47'),(265,'Power-Tv','0','2020-04-08 13:47:04'),(266,'Power-Tv','1','2020-04-08 13:47:16'),(267,'Power-Tv','0','2020-04-08 13:48:21'),(268,'Power-Tv','1','2020-04-08 13:51:55'),(269,'Power-Tv','0','2020-04-08 15:44:20'),(270,'Power-Tv','1','2020-04-08 15:46:20'),(271,'Power-Tv','0','2020-04-08 15:50:15'),(272,'Power-Tv','1','2020-04-08 15:50:17'),(273,'Power-Tv','0','2020-04-08 15:50:24'),(274,'Power-Tv','1','2020-04-08 15:50:25'),(275,'Power-Tv','0','2020-04-08 15:50:47'),(276,'Power-Tv','1','2020-04-08 15:50:51'),(277,'Power-Tv','0','2020-04-08 15:51:02'),(278,'Power-Tv','1','2020-04-08 15:51:05'),(279,'Power-Tv','0','2020-04-08 15:51:10'),(280,'Power-Tv','1','2020-04-08 15:52:59'),(281,'Power-Tv','0','2020-04-08 15:53:00'),(282,'Power-Tv','1','2020-04-08 15:54:43'),(283,'Power-Tv','0','2020-04-08 15:55:32'),(284,'Power-Tv','1','2020-04-08 16:01:44'),(285,'Volume-Tv','1','2020-04-08 16:01:56'),(286,'Canal-Tv','1','2020-04-08 16:02:07'),(287,'Volume-Tv','1','2020-04-08 16:02:34'),(288,'Volume-Tv','1','2020-04-08 16:02:48'),(289,'Volume-Tv','0','2020-04-08 16:02:52'),(290,'Power-Tv','0','2020-04-08 16:03:10'),(291,'Power-Tv','1','2020-04-08 16:06:24'),(292,'Power-Tv','0','2020-04-08 16:06:52'),(293,'Power-Tv','1','2020-04-08 16:07:24'),(294,'Power-Tv','0','2020-04-08 16:07:32'),(295,'Power-Tv','1','2020-04-08 16:08:14'),(296,'Power-Tv','0','2020-04-08 16:08:17'),(297,'Power-Tv','1','2020-04-08 16:10:00'),(298,'Power-Tv','0','2020-04-08 16:10:11'),(299,'Power-Tv','1','2020-04-08 16:11:14'),(300,'Power-Tv','0','2020-04-08 16:11:33'),(301,'Power-Tv','1','2020-04-08 16:11:44'),(302,'Power-Tv','0','2020-04-08 16:11:48'),(303,'Power-Tv','1','2020-04-08 16:36:14'),(304,'Power-Tv','0','2020-04-08 16:36:51'),(305,'Power-Tv','1','2020-04-08 16:37:18'),(306,'Power-Tv','0','2020-04-08 16:38:21'),(307,'Power-Tv','1','2020-04-08 16:38:28'),(308,'Power-Tv','0','2020-04-08 16:39:12'),(309,'Power-Tv','1','2020-04-08 16:39:42'),(310,'Power-Tv','0','2020-04-08 16:41:01'),(311,'Power-Tv','1','2020-04-08 16:41:12'),(312,'Power-Tv','0','2020-04-08 16:41:42'),(313,'Power-Tv','1','2020-04-08 16:41:54'),(314,'Power-Tv','0','2020-04-08 16:50:41'),(315,'Power-Tv','1','2020-04-08 16:50:56'),(316,'Power-Tv','0','2020-04-08 16:51:23'),(317,'Power-Tv','1','2020-04-08 16:51:57'),(318,'Power-Tv','0','2020-04-08 16:52:04'),(319,'Power-Tv','1','2020-04-08 16:56:23'),(320,'Power-Tv','0','2020-04-08 16:56:34'),(321,'Power-Tv','1','2020-04-08 16:56:41'),(322,'Power-Tv','0','2020-04-08 16:56:48'),(323,'Power-Tv','1','2020-04-08 17:00:15'),(324,'Power-Tv','0','2020-04-08 17:00:38'),(325,'Power-Tv','1','2020-04-08 17:00:40'),(326,'Power-Tv','0','2020-04-08 17:02:44'),(327,'Power-Tv','1','2020-04-08 17:07:38'),(328,'Power-Tv','0','2020-04-08 17:07:47'),(329,'Power-Tv','1','2020-04-08 17:08:10'),(330,'Power-Tv','0','2020-04-08 17:08:16'),(331,'Power-Tv','1','2020-04-08 17:08:25'),(332,'Power-Tv','0','2020-04-08 17:10:35'),(333,'Power-Tv','1','2020-04-08 17:10:46'),(334,'Power-Tv','0','2020-04-08 17:11:00'),(335,'Power-Tv','1','2020-04-08 17:11:18'),(336,'Power-Tv','0','2020-04-08 17:11:35'),(337,'Power-Tv','1','2020-04-08 17:12:14'),(338,'Power-Tv','0','2020-04-08 17:20:41'),(339,'Power-Tv','1','2020-04-08 17:20:51'),(340,'Power-Tv','0','2020-04-08 17:21:21'),(341,'Power-Tv','1','2020-04-08 17:27:49'),(342,'Power-Tv','0','2020-04-09 21:33:18'),(343,'Power-Tv','1','2020-04-09 21:33:24'),(344,'Power-Tv','0','2020-04-12 13:47:29'),(345,'Power-Tv','1','2020-04-12 14:43:00'),(346,'Power-Tv','0','2020-04-12 14:43:03'),(347,'Power-Tv','1','2020-04-12 14:56:58'),(348,'Power-Tv','0','2020-04-12 14:57:04'),(349,'Power-Tv','1','2020-04-12 14:57:07'),(350,'Power-Tv','0','2020-04-12 14:57:10'),(351,'Power-Tv','1','2020-04-12 19:10:28'),(352,'Power-Tv','0','2020-04-12 19:10:32'),(353,'Power-Tv','1','2020-04-12 21:00:51'),(354,'Power-Tv','0','2020-04-12 21:00:53'),(355,'Iluminacao','1','2020-04-12 22:53:01'),(356,'Iluminacao','0','2020-04-12 22:53:23'),(357,'Iluminacao','1','2020-04-12 23:19:16'),(358,'Iluminacao','1','2020-04-12 23:20:00'),(359,'Iluminacao','1','2020-04-12 23:24:16'),(360,'Iluminacao','1','2020-04-12 23:34:38'),(361,'Iluminacao','1','2020-04-12 23:35:23'),(362,'Iluminacao','0','2020-04-12 23:36:32'),(363,'Iluminacao','1','2020-04-12 23:36:37'),(364,'Iluminacao','0','2020-04-12 23:38:11'),(365,'Iluminacao','1','2020-04-12 23:38:54'),(366,'Iluminacao','0','2020-04-12 23:39:08'),(367,'Iluminacao','1','2020-04-12 23:39:16'),(368,'Iluminacao','1','2020-04-12 23:39:50'),(369,'Iluminacao','1','2020-04-12 23:42:00'),(370,'Iluminacao','0','2020-04-12 23:42:14'),(371,'Iluminacao','1','2020-04-12 23:43:26'),(372,'Iluminacao','0','2020-04-12 23:43:32'),(373,'Iluminacao','1','2020-04-12 23:43:52'),(374,'Iluminacao','0','2020-04-12 23:47:03'),(375,'Iluminacao','1','2020-04-12 23:47:07'),(376,'Iluminacao','0','2020-04-13 00:05:39'),(377,'Power-Tv','1','2020-04-13 00:06:22'),(378,'Power-Tv','0','2020-04-13 00:06:29'),(379,'Power-Tv','1','2020-04-13 00:06:38'),(380,'Power-Tv','0','2020-04-13 00:06:41'),(381,'Iluminacao','1','2020-04-13 11:36:31'),(382,'Iluminacao','0','2020-04-13 11:37:19'),(383,'Power-Tv','1','2020-04-13 15:10:55'),(384,'Power-Tv','0','2020-04-13 15:10:58'),(385,'Iluminacao','1','2020-04-13 17:17:29'),(386,'Iluminacao','0','2020-04-13 17:17:45'),(387,'Iluminacao','1','2020-04-13 17:19:25'),(388,'Iluminacao','0','2020-04-13 19:17:56'),(389,'Iluminacao','1','2020-04-13 19:18:34'),(390,'Iluminacao','0','2020-04-13 19:20:17'),(391,'Iluminacao','1','2020-04-13 19:21:05'),(392,'Iluminacao','0','2020-04-13 19:21:46'),(393,'Iluminacao','1','2020-04-13 19:44:29'),(394,'Iluminacao','0','2020-04-13 19:44:53'),(395,'Iluminacao','1','2020-04-13 19:46:09'),(396,'Iluminacao','0','2020-04-13 19:46:13'),(397,'Iluminacao','1','2020-04-13 19:46:23'),(398,'Iluminacao','0','2020-04-13 19:46:45'),(399,'Iluminacao','1','2020-04-13 19:48:58'),(400,'Iluminacao','0','2020-04-13 19:49:47'),(401,'Power-Ar-Off','0','2020-04-17 14:55:18'),(402,'Power-Ar-Off','0','2020-04-17 17:00:22'),(403,'Power-Ar-Off','0','2020-04-17 17:01:25'),(404,'Power-Ar-Off','0','2020-04-17 17:59:45');
/*!40000 ALTER TABLE `historico_acoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iot_project`
--

DROP TABLE IF EXISTS `iot_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iot_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `horario` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `corrente` double NOT NULL,
  `tensao` double NOT NULL,
  `potencia` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=381 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iot_project`
--

LOCK TABLES `iot_project` WRITE;
/*!40000 ALTER TABLE `iot_project` DISABLE KEYS */;
INSERT INTO `iot_project` VALUES (209,'2020-04-09 22:07:38',4.96,155.98,773.47),(208,'2020-04-09 22:07:20',5.5,130.3,716.45),(207,'2020-04-09 22:07:03',5.04,123.79,623.73),(206,'2020-04-09 22:06:46',4.63,128.2,593.87),(205,'2020-04-09 22:06:29',5.49,127.37,699.79),(204,'2020-04-09 22:06:12',5.99,105.88,634.24),(203,'2020-04-09 22:05:55',5.92,124.21,735.87),(202,'2020-04-09 22:05:38',5.2,124.54,647.27),(201,'2020-04-09 22:05:21',5.38,126.44,680.23),(200,'2020-04-09 22:05:04',5,124.38,621.9),(199,'2020-04-09 22:04:47',5.44,123.55,672.52),(198,'2020-04-09 22:04:30',5.33,125.06,666.97),(197,'2020-04-09 22:04:13',4.8,114.93,551.61),(196,'2020-04-09 22:03:55',5.58,128.17,715.37),(195,'2020-04-09 22:03:38',5.64,138.73,782.77),(194,'2020-04-09 22:03:21',5.62,116.07,652.03),(193,'2020-04-09 22:03:04',5.02,126.63,635.86),(192,'2020-04-09 22:02:47',5.77,128.81,743.3),(191,'2020-04-09 22:02:30',5.48,124.55,681.98),(190,'2020-04-09 22:02:13',5.67,118.37,671.29),(189,'2020-04-09 22:01:56',5.52,123.93,684.37),(188,'2020-04-09 22:01:39',5.02,127.2,638.1),(187,'2020-04-09 22:01:22',5.46,133.13,726.96),(186,'2020-04-09 22:01:05',5.52,128.01,706.82),(185,'2020-04-09 22:00:47',4.68,97.62,456.75),(184,'2020-04-09 22:00:30',5.38,129.88,699.31),(183,'2020-04-09 22:00:13',5.35,126.1,674.93),(182,'2020-04-09 21:59:56',4.85,145.23,705.02),(181,'2020-04-09 21:59:39',5.72,128.4,734.61),(180,'2020-04-09 21:59:22',5.46,121.98,665.48),(179,'2020-04-09 21:59:05',4.83,133.99,647.8),(178,'2020-04-09 21:58:48',5.24,116.47,609.84),(177,'2020-04-09 21:58:31',5.68,187.7,1065.84),(176,'2020-04-09 21:58:14',14.62,367.17,5369.76),(175,'2020-04-09 21:57:56',146.73,762.93,111942.43),(210,'2020-04-09 22:07:55',5.37,157.86,846.96),(211,'2020-04-09 22:08:12',5.39,126.13,679.75),(212,'2020-04-09 22:08:29',5.46,177.2,968.41),(213,'2020-04-09 22:08:47',5.76,128.65,741.49),(214,'2020-04-09 22:09:04',5.26,127.29,669.18),(215,'2020-04-09 22:09:21',5.4,112.61,607.89),(216,'2020-04-09 22:09:38',4.78,123.98,592.39),(217,'2020-04-09 22:09:55',5.33,123.57,658.22),(218,'2020-04-09 22:10:12',4.99,170.34,849.24),(219,'2020-04-09 22:10:29',4.6,111.5,512.91),(220,'2020-04-09 22:10:46',4.37,145.41,635.57),(221,'2020-04-09 22:11:03',4.76,134.73,641.12),(222,'2020-04-09 22:11:20',5.24,121.32,636.04),(223,'2020-04-09 22:11:38',4.88,123.24,601.26),(224,'2020-04-09 22:11:55',4.98,123.57,615.92),(225,'2020-04-09 22:12:12',5.3,109.17,578.2),(226,'2020-04-09 22:12:29',5.06,112.29,568.37),(227,'2020-04-09 22:12:46',5.1,117.79,600.59),(228,'2020-04-09 22:13:03',5.44,133.8,728.17),(229,'2020-04-09 22:13:20',5.08,170.81,868.13),(230,'2020-04-09 22:13:37',5.02,125.45,629.81),(231,'2020-04-09 22:13:54',5.24,126.92,665.07),(232,'2020-04-09 22:14:11',5.25,169.62,889.98),(233,'2020-04-09 22:14:28',5.26,108.51,571.13),(234,'2020-04-09 22:14:45',5.26,128.14,673.88),(235,'2020-04-09 22:15:02',5.7,115.52,658.57),(236,'2020-04-09 22:15:19',4.99,171.6,855.61),(237,'2020-04-09 22:15:36',5.24,124.98,654.69),(238,'2020-04-09 22:15:54',5.08,108.01,548.46),(239,'2020-04-09 22:16:11',5.31,126.92,674.42),(240,'2020-04-09 22:16:28',5.2,127.12,660.54),(241,'2020-04-09 22:16:45',5.26,159.85,840.71),(242,'2020-04-09 22:17:02',5.61,119.32,669.84),(243,'2020-04-09 22:17:19',6.36,149.14,948.39),(244,'2020-04-09 22:17:36',5.28,124.39,656.88),(245,'2020-04-09 22:17:53',5.64,126.09,711.71),(246,'2020-04-09 22:18:10',5.34,124.85,666.37),(247,'2020-04-09 22:18:27',5.54,125.06,692.42),(248,'2020-04-09 22:18:44',5.91,150.69,890.9),(249,'2020-04-09 22:19:01',6.22,126.16,785.01),(250,'2020-04-09 22:19:18',5.57,126.8,706.05),(251,'2020-04-09 22:19:35',5.15,136.34,702.72),(252,'2020-04-09 22:19:52',6.2,118.84,737.13),(253,'2020-04-09 22:20:09',7.08,159.39,1128.64),(254,'2020-04-09 22:20:26',5.72,125.04,715.1),(255,'2020-04-09 22:20:44',5.49,127.58,700.56),(256,'2020-04-09 22:21:01',5.68,133.02,755.13),(257,'2020-04-09 22:21:18',6.14,127.26,781.45),(258,'2020-04-09 22:21:35',5.58,127.7,712.79),(259,'2020-04-09 22:21:52',5.56,122.82,683.08),(260,'2020-04-09 22:22:09',5.75,132.59,761.92),(261,'2020-04-09 22:22:26',5.01,125.81,629.99),(262,'2020-04-09 22:22:43',6.02,135.79,817.15),(263,'2020-04-09 22:23:00',5.57,141.27,786.4),(264,'2020-04-09 22:23:17',5.68,126.32,718.04),(265,'2020-04-09 22:23:34',4.84,131.85,638.42),(266,'2020-04-09 22:23:51',5.46,131.87,719.4),(267,'2020-04-09 22:24:08',5.6,117.38,657.3),(268,'2020-04-09 22:24:25',5.49,124.34,683.01),(269,'2020-04-09 22:24:42',5.51,153.59,845.58),(270,'2020-04-09 22:24:59',5.86,123.33,722.6),(271,'2020-04-09 22:25:16',5.82,109.32,636.59),(272,'2020-04-09 22:25:34',5.5,109.7,602.86),(273,'2020-04-09 22:25:51',6.22,127.82,795.67),(274,'2020-04-09 22:26:08',4.8,158.52,760.33),(275,'2020-04-09 22:26:25',6.25,127.83,798.77),(276,'2020-04-09 22:26:42',4.88,126.13,615.29),(277,'2020-04-09 22:26:59',5.5,129.35,711.88),(278,'2020-04-09 22:27:16',5.8,85.21,494.34),(279,'2020-04-09 22:27:33',5.33,125.8,670.74),(280,'2020-04-09 22:27:50',5.29,127.24,672.88),(281,'2020-04-09 22:28:07',5.98,128.15,766.72),(282,'2020-04-09 22:28:24',5.38,123.91,667.04),(283,'2020-04-09 22:28:41',4.88,118.43,577.54),(284,'2020-04-09 22:28:58',5.54,125.56,695.6),(285,'2020-04-09 22:29:15',5.88,113.43,667.36),(286,'2020-04-09 22:29:32',5.68,115.12,653.84),(287,'2020-04-09 22:29:50',5.43,118.47,643.07),(288,'2020-04-09 22:30:07',5.51,176.11,970.47),(289,'2020-04-09 22:30:24',5.65,125.82,711.13),(290,'2020-04-09 22:30:41',5.8,124.11,720.41),(291,'2020-04-09 22:30:58',5.54,107.82,597.57),(292,'2020-04-09 22:31:15',5.53,128.59,711.21),(293,'2020-04-09 22:31:32',5.74,127.63,733.05),(294,'2020-04-09 22:31:49',6.23,117.72,733.78),(295,'2020-04-09 22:32:06',5.47,172.61,944.17),(296,'2020-04-09 22:32:23',5.98,139.96,837.6),(297,'2020-04-09 22:32:40',5.6,116.98,654.53),(298,'2020-04-09 22:32:57',5.2,112.03,582.94),(299,'2020-04-09 22:33:14',5.04,123.81,623.42),(300,'2020-04-09 22:33:31',5.66,119.22,674.31),(301,'2020-04-09 22:33:48',5.85,124.47,727.8),(302,'2020-04-09 22:34:05',4.85,124.11,602.26),(303,'2020-04-09 22:34:23',5.66,124.23,703.16),(304,'2020-04-09 22:34:40',5.42,140.2,759.83),(305,'2020-04-09 22:34:57',5.26,118.74,624.8),(306,'2020-04-09 22:35:14',5.78,119.86,692.58),(307,'2020-04-09 22:35:31',5.47,123.87,677.13),(308,'2020-04-09 22:35:48',6.17,124.87,770.18),(309,'2020-04-09 22:36:05',5.74,192.57,1105.1),(310,'2020-04-09 22:36:22',5.1,123.52,629.54),(311,'2020-04-09 22:36:39',4.92,120.27,591.41),(312,'2020-04-09 22:36:56',5.14,122.73,630.23),(313,'2020-04-09 22:37:13',5.69,126.59,720.03),(314,'2020-04-09 22:37:30',5.75,149.93,862.56),(315,'2020-04-09 22:37:47',5.9,123.4,727.99),(316,'2020-04-09 22:38:04',5.5,124.18,683.02),(317,'2020-04-09 22:38:21',5.4,124.22,670.49),(318,'2020-04-09 22:38:38',5.61,95.9,538.07),(319,'2020-04-09 22:38:56',5.76,125.54,722.74),(320,'2020-04-09 22:39:13',5.71,124.55,711.31),(321,'2020-04-09 22:39:30',5.5,114.78,631),(322,'2020-04-09 22:39:47',5.6,124.85,699.22),(323,'2020-04-09 22:40:04',5.57,124.34,692.18),(324,'2020-04-09 22:40:21',5.01,121.17,607.67),(325,'2020-04-09 22:40:38',5.42,124.78,676.57),(326,'2020-04-09 22:40:55',5.33,122.84,655.05),(327,'2020-04-09 22:41:12',5.72,118.08,675.03),(328,'2020-04-09 22:41:29',5.37,119.85,643.08),(329,'2020-04-09 22:41:47',5.61,125.39,703.52),(330,'2020-04-09 22:42:04',5.99,125.02,748.32),(331,'2020-04-09 22:42:21',5.52,111.42,615.55),(332,'2020-04-09 22:42:38',5.25,124.59,654.67),(333,'2020-04-09 22:42:55',5.46,159.04,868.34),(334,'2020-04-09 22:43:12',5.16,133.62,689.82),(335,'2020-04-09 22:43:29',5.41,117.22,634.56),(336,'2020-04-09 22:43:46',5.28,124.98,659.33),(337,'2020-04-09 22:44:03',6.04,127.04,767.36),(338,'2020-04-09 22:44:21',4.92,163.42,803.49),(339,'2020-04-09 22:44:38',5.72,151.41,866.33),(340,'2020-04-09 22:44:55',5.38,164.36,883.66),(341,'2020-04-09 22:45:12',4.86,123.27,599.1),(342,'2020-04-09 22:45:29',5.51,114.1,628.12),(343,'2020-04-09 22:45:46',5.28,129.3,683.27),(344,'2020-04-09 22:46:03',5.63,115.59,650.49),(345,'2020-04-09 22:46:20',5.91,146.07,862.96),(346,'2020-04-09 22:46:37',4.8,124.59,597.46),(347,'2020-04-09 22:46:54',5.19,117.9,611.59),(348,'2020-04-09 22:47:11',5.58,144.1,804.57),(349,'2020-04-09 22:47:28',5.15,119.64,615.56),(350,'2020-04-09 22:47:45',5.45,123.96,676.1),(351,'2020-04-09 22:48:02',5.42,129.79,703.36),(352,'2020-04-09 22:48:19',4.79,169,809.56),(353,'2020-04-09 22:48:36',5.66,116.39,658.58),(354,'2020-04-09 22:48:54',5.23,113.78,594.86),(355,'2020-04-09 22:49:11',5.29,136.67,722.67),(356,'2020-04-09 22:49:28',5.62,124.73,700.99),(357,'2020-04-09 22:49:45',5.31,166.06,882.1),(358,'2020-04-09 22:50:02',5.78,109.61,633.38),(359,'2020-04-09 22:50:19',5.43,120.66,655.05),(360,'2020-04-09 22:50:36',5.55,168.91,936.87),(361,'2020-04-09 22:50:53',5.57,127.99,712.76),(362,'2020-04-09 22:51:10',4.88,118.21,576.77),(363,'2020-04-10 00:11:26',235.49,936.98,220651.71),(364,'2020-04-10 00:11:43',53.95,903.99,48766.24),(365,'2020-04-10 00:12:00',13.22,862.36,11403.06),(366,'2020-04-10 00:12:17',7.94,820.4,6512.23),(367,'2020-04-10 00:12:34',6.8,620.88,4219.59),(368,'2020-04-10 00:12:52',6.51,331.92,2160.92),(369,'2020-04-10 00:13:09',8.68,221.43,1921.62),(370,'2020-04-10 00:13:26',7.92,150.99,1196.44),(371,'2020-04-10 00:13:44',7.52,107.48,808.24),(372,'2020-04-10 00:14:01',7.23,82.44,596.03),(373,'2020-04-10 00:14:18',7.4,70.87,524.29),(374,'2020-04-10 00:14:36',7.92,39.48,312.65),(375,'2020-04-10 00:14:53',7.53,53.11,399.84),(376,'2020-04-10 00:15:10',7.86,51.9,407.98),(377,'2020-04-10 00:15:27',7.38,49.4,364.82),(378,'2020-04-10 00:15:44',7.69,49.93,384.04),(379,'2020-04-10 00:16:01',7.5,33.66,252.27),(380,'2020-04-10 00:16:18',7.49,14.18,106.25);
/*!40000 ALTER TABLE `iot_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicao`
--

DROP TABLE IF EXISTS `medicao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `horario` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `corrente` double NOT NULL,
  `tensao` double NOT NULL,
  `potencia` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1990 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicao`
--

LOCK TABLES `medicao` WRITE;
/*!40000 ALTER TABLE `medicao` DISABLE KEYS */;
INSERT INTO `medicao` VALUES (1983,'2020-04-21 20:58:55',0.86,125.36,5434.64),(1980,'2020-04-21 23:55:57',0.28,127.81,1716.06),(1984,'2020-04-21 19:59:56',0.84,124.75,2587),(1985,'2020-04-21 18:00:00',0.679,124.833,592.19),(1982,'2020-04-21 21:00:00',0.809,125.278,5064.33),(1981,'2020-04-21 22:59:20',0.29,127.24,3144.19),(1989,'2020-04-21 14:00:00',1.122,125.501,4082.75),(1988,'2020-04-21 15:58:55',1.15,124.93,6922.46),(1486,'2020-04-16 20:58:57',1.19,124.49,774.25),(1487,'2020-04-16 19:43:33',10,5,20),(1987,'2020-04-21 16:51:52',0.78,125.99,5172.38),(1986,'2020-04-21 17:26:32',0.77,126.3,1263.41),(1592,'2020-04-17 14:59:20',0.18,125.13,903.23),(1584,'2020-04-17 22:38:01',0.22,122.08,828.95),(1585,'2020-04-17 21:59:21',0.19,123.76,1318.82),(1586,'2020-04-17 20:00:00',0.174,125.557,1073.79),(1587,'2020-04-17 19:00:00',0.165,124.26,1023.01),(1588,'2020-04-17 18:00:00',0.168,124.172,1039.56),(1589,'2020-04-17 17:00:00',0.189,124.813,1183.76),(1590,'2020-04-17 16:58:50',0.19,124.94,1106.24),(1123,'2020-04-14 20:58:51',3.79,12.88,105156.67),(1122,'2020-04-14 21:59:30',4.88,6.38,70241.77),(1121,'2020-04-14 22:00:00',6.336,13.411,83561.24),(1120,'2020-04-14 23:00:00',5.659,15.771,84061.27),(1119,'2020-04-15 00:00:00',5.508,14.765,69716.97),(1118,'2020-04-15 01:58:41',5.97,61.82,69919.97),(1485,'2020-04-16 21:59:07',0.98,125.1,5385.66),(1117,'2020-04-15 02:39:17',6.02,19.9,52960.67),(1116,'2020-04-15 16:58:41',4.31,140.41,123842.71),(1115,'2020-04-15 17:48:37',5.36,133.03,254055.35),(1114,'2020-04-15 18:27:25',5.28,143.42,23279.33),(1113,'2020-04-15 22:59:06',4.44,129.16,359356.3),(1112,'2020-04-15 23:58:14',4.42,128.78,351072.93),(1111,'2020-04-16 00:11:54',3.36,179.47,89164.95),(1110,'2020-04-16 01:59:24',1.49,127.09,246797.32),(1109,'2020-04-16 02:09:02',0.94,181.68,45104.04),(1480,'2020-04-17 02:19:34',0.16,125.22,306.77),(1481,'2020-04-17 01:59:03',0.15,125.55,893.69),(1488,'2020-04-16 18:49:52',12,14,10),(1482,'2020-04-17 00:59:56',0.14,126.26,983.38),(1483,'2020-04-16 23:00:00',0.149,124.553,926.29),(1484,'2020-04-16 22:59:15',0.15,124.45,3050.6),(1591,'2020-04-17 15:59:42',0.15,125.91,1276.17);
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
  `dia` int(11) NOT NULL,
  `valor` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3982 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tendencias`
--

LOCK TABLES `tendencias` WRITE;
/*!40000 ALTER TABLE `tendencias` DISABLE KEYS */;
INSERT INTO `tendencias` VALUES (3978,'Temperatura-Ar-Mais','1900-01-01 09:14:49',2,15),(3981,'Power-Ar-On','1900-01-01 16:26:44',0,7),(3979,'Temperatura-Ar-Menos','1900-01-01 16:34:18',0,13),(3977,'Temperatura-Ar-Mais','1900-01-01 16:23:46',0,11);
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

-- Dump completed on 2020-04-22  0:09:15
