-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: voluntariado_schema
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `misiones`
--

DROP TABLE IF EXISTS `misiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `misiones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `fecha` date NOT NULL,
  `voluntarios_necesarios` int NOT NULL,
  `descripcion` text NOT NULL,
  `usuario_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `misiones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `misiones`
--

LOCK TABLES `misiones` WRITE;
/*!40000 ALTER TABLE `misiones` DISABLE KEYS */;
INSERT INTO `misiones` VALUES (1,'mision 1','2025-12-06',3,'Correr 5km',2,'2025-12-06 00:27:27','2025-12-06 00:27:27'),(2,'mision2','2025-12-06',2,'123',4,'2025-12-06 01:04:47','2025-12-06 01:04:47'),(3,'qwe','2026-12-12',3,'qsd',5,'2025-12-06 04:29:08','2025-12-06 04:29:08'),(5,'1221','2025-12-25',2,'editado\r\n',1,'2025-12-06 04:48:18','2025-12-06 04:48:26');
/*!40000 ALTER TABLE `misiones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'anibal','sierra','anibalsierra@me.com','$2b$12$Ifvv9MllbasDoG6W.rs8oOSBlF74ZYwcw8Q.jYR/ts.NmwAqlgx9i','2025-12-06 00:23:29','2025-12-06 00:23:29'),(2,'anibal','sierra','anibalsierra@you.com','$2b$12$xncB21aS.vlxhnGhafeekOSpMhG/H2pDP8BYypbCxGm4/7jKbW016','2025-12-06 00:24:47','2025-12-06 00:24:47'),(3,'algo','cosa','algo@cosa.cl','$2b$12$NUu1dJBoBimDN1h1aYyfLO93KXCBmuJSrM8aSfXyXMnLvUjfpxQTK','2025-12-06 00:53:49','2025-12-06 00:53:49'),(4,'hola','como','estas@tu.com','$2b$12$SEJBsKJDcZOX6bwedacmL.AIbyUjsLW/gJ2s/Lfax2.KLfoE27shS','2025-12-06 00:54:52','2025-12-06 00:54:52'),(5,'probando','123','as@as.cl','$2b$12$ssgm7bjKBdt/MJhqsrKoWu6ICPvps0txY6/CpmWBVqMXqmTeQrIQ6','2025-12-06 04:27:51','2025-12-06 04:27:51'),(6,'Diego','Sierra','diegosierra@me.com','$2b$12$Gsoiw43PUUoz61yl6cXhdOxxciLTuNLG3bNlECF.wHx.rUvibvqQG','2025-12-06 04:59:09','2025-12-06 04:59:09');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voluntarios_misiones`
--

DROP TABLE IF EXISTS `voluntarios_misiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `voluntarios_misiones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `mision_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `mision_id` (`mision_id`),
  CONSTRAINT `voluntarios_misiones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `voluntarios_misiones_ibfk_2` FOREIGN KEY (`mision_id`) REFERENCES `misiones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voluntarios_misiones`
--

LOCK TABLES `voluntarios_misiones` WRITE;
/*!40000 ALTER TABLE `voluntarios_misiones` DISABLE KEYS */;
INSERT INTO `voluntarios_misiones` VALUES (1,4,1,'2025-12-06 01:04:50'),(2,4,2,'2025-12-06 01:06:16'),(3,1,1,'2025-12-06 04:24:46'),(4,5,1,'2025-12-06 04:33:46'),(5,5,3,'2025-12-06 04:33:55'),(6,1,2,'2025-12-06 04:57:56'),(7,6,1,'2025-12-06 04:59:18');
/*!40000 ALTER TABLE `voluntarios_misiones` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-06  5:46:37
