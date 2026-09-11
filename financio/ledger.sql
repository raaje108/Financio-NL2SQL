-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: ledger
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
-- Temporary view structure for view `shop_activity_status`
--

DROP TABLE IF EXISTS `shop_activity_status`;
/*!50001 DROP VIEW IF EXISTS `shop_activity_status`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `shop_activity_status` AS SELECT 
 1 AS `shop_id`,
 1 AS `shop_name`,
 1 AS `phone_no`,
 1 AS `last_purchase_date`,
 1 AS `is_active`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `shop_inventory`
--

DROP TABLE IF EXISTS `shop_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shop_inventory` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `shop_id` int NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `quantity` int DEFAULT '0',
  `price` decimal(10,2) NOT NULL,
  `total_amount` decimal(10,2) GENERATED ALWAYS AS ((`quantity` * `price`)) VIRTUAL,
  `amount_paid` decimal(10,2) DEFAULT '0.00',
  `amount_rem` decimal(10,2) GENERATED ALWAYS AS ((`total_amount` - coalesce(`amount_paid`,0))) VIRTUAL,
  `entry_date` date DEFAULT (curdate()),
  `payment_method` varchar(50) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`item_id`),
  KEY `shop_id` (`shop_id`),
  CONSTRAINT `inventory_shop_fk` FOREIGN KEY (`shop_id`) REFERENCES `shops` (`shop_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_inventory`
--

LOCK TABLES `shop_inventory` WRITE;
/*!40000 ALTER TABLE `shop_inventory` DISABLE KEYS */;
/*!40000 ALTER TABLE `shop_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shops`
--

DROP TABLE IF EXISTS `shops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shops` (
  `shop_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `shop_name` varchar(100) NOT NULL,
  `shop_address` text,
  `shop_owner` varchar(100) DEFAULT NULL,
  `phone_no` varchar(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `shop_category` varchar(50) DEFAULT 'general',
  PRIMARY KEY (`shop_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `shops_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shops`
--

LOCK TABLES `shops` WRITE;
/*!40000 ALTER TABLE `shops` DISABLE KEYS */;
/*!40000 ALTER TABLE `shops` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `shop_id` int NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `transaction_type` enum('PAYMENT_RECEIVED','REFUND_ISSUED') NOT NULL DEFAULT 'PAYMENT_RECEIVED',
  `payment_method` varchar(50) DEFAULT 'CASH',
  `transaction_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `notes` text,
  PRIMARY KEY (`transaction_id`),
  KEY `shop_id` (`shop_id`),
  CONSTRAINT `transaction_shop_fk` FOREIGN KEY (`shop_id`) REFERENCES `shops` (`shop_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `phone_no` varchar(20) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `role` varchar(100) DEFAULT 'Business Account & Primary Admin',
  `about` text,
  `address` text,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'keshav','keshav@gmail.com','1111111111','$2b$10$Wv8kxJ0B4mfClb8HI56KWuFzj74kf3NgAEHcoUcrNlB8Mc43xdfLC','2026-03-27 11:19:05','Business Account & Primary Admin',NULL,NULL,NULL),(2,'keshav','keshav1@gmail.com','1111111111','$2b$10$0SXaZsf7TH2hbKbuqsWoxuZSDHRqHtocbXiOBY0GnfR9PBRWZwaQe','2026-03-27 11:27:31','Business Account & Primary Admin',NULL,NULL,NULL),(3,'keshav','keshav2@gmail.com','1111111111','$2b$10$g9gq0zS8R3XVDlC.eHpK3uEgPa8pav9bhrS9dTSQo49x.xfdEgnXG','2026-03-27 16:16:22','Business Account & Primary Admin',NULL,NULL,NULL),(4,'lol','lol@gmail.com','0000000000','$2b$10$4wWOuiMnM4Zm9Ejv1lcIceE86LvIw38OmmyatS7Wluyjd1MAQFgKy','2026-04-08 18:45:46','Business Account & Primary Admin',NULL,NULL,NULL),(5,'keshav bhardwaj','k2@gmail.com','0000000000','$2b$10$1Dvr45Zkt/PvHAJvUpZLB.rxF2.GtcAcr478oYekdG8idGxRIlm2a','2026-04-08 19:41:11','Business Account & Primary Admin',NULL,NULL,NULL),(6,'king','k3@gmail.com','0000000000','$2b$10$121l6XsAPB9SkP/P.S8fdOgf7SKpnPMxxEz6t6h2Gg1nHMKzvQFGq','2026-04-08 19:45:12','Business Account & Primary Admin',NULL,NULL,NULL),(7,'king','k4@gmail.com','0000000000','$2b$10$fgp8Uogr6xkNS0o3R2a9uuf85es.iLoTJF26XaM4s3.tlpnqPvzqK','2026-04-08 19:50:01','Business Account & Primary Admin',NULL,NULL,NULL),(8,'king','k5@gmail.com','0000000000','$2b$10$0ETUo48pT71cCPNyxqQM.OteQKykduTgDnvUnTqocRaGQ68MF3GyC','2026-04-08 19:51:33','Business Account & Primary Admin',NULL,NULL,NULL),(9,'king','k6@gmail.com','0000000000','$2b$10$5h336a2Ro9xowUrEHvRHVOEA5Kb5DkNFdiCr6UJiRze40h8Y2ctOC','2026-04-08 19:56:03','Business Account & Primary Admin',NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'ledger'
--

--
-- Final view structure for view `shop_activity_status`
--

/*!50001 DROP VIEW IF EXISTS `shop_activity_status`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `shop_activity_status` AS select `s`.`shop_id` AS `shop_id`,`s`.`shop_name` AS `shop_name`,`s`.`phone_no` AS `phone_no`,max(`i`.`entry_date`) AS `last_purchase_date`,if((max(`i`.`entry_date`) >= (curdate() - interval 3 month)),true,false) AS `is_active` from (`shops` `s` left join `shop_inventory` `i` on((`s`.`shop_id` = `i`.`shop_id`))) group by `s`.`shop_id`,`s`.`shop_name`,`s`.`phone_no` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-09 12:50:03
