CREATE DATABASE  IF NOT EXISTS `esg_database` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `esg_database`;
-- MySQL dump 10.13  Distrib 8.0.38, for macos14 (arm64)
--
-- Host: localhost    Database: esg_database
-- ------------------------------------------------------
-- Server version	9.0.1

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
-- Table structure for table `ESG_Report`
--

DROP TABLE IF EXISTS `ESG_Report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ESG_Report` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `firm_name` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `report_name` varchar(255) NOT NULL,
  `report_year` year NOT NULL,
  `report_path` varchar(255) NOT NULL,
  `upload_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`report_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ESG_Report`
--

LOCK TABLES `ESG_Report` WRITE;
/*!40000 ALTER TABLE `ESG_Report` DISABLE KEYS */;
INSERT INTO `ESG_Report` VALUES (1,'Example Firm','Example User','2023 ESG Report',2023,'/path/to/report.pdf','2024-11-13 04:31:51'),(2,'Example Firm','Example User','2023 ESG Report',2023,'/path/to/report.pdf','2024-11-13 04:35:56'),(3,'NUS','sxy','NUS 2022 ESG Report 20241113124106.pdf',2022,'pdf_processing/uploads/NUS 2022 ESG Report 20241113124106.pdf','2024-11-13 04:41:06'),(4,'abc','sxy','abc 2022 ESG Report 20241113124809.pdf',2022,'pdf_processing/uploads/abc 2022 ESG Report 20241113124809.pdf','2024-11-13 04:48:09');
/*!40000 ALTER TABLE `ESG_Report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ESG_Scores`
--

DROP TABLE IF EXISTS `ESG_Scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ESG_Scores` (
  `score_id` int NOT NULL AUTO_INCREMENT,
  `report_id` int DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `Total_Score` decimal(5,2) DEFAULT NULL,
  `Rating` varchar(50) DEFAULT NULL,
  `E_Score` decimal(5,2) DEFAULT NULL,
  `S_Score` decimal(5,2) DEFAULT NULL,
  `G_Score` decimal(5,2) DEFAULT NULL,
  `Emission_intensities` decimal(10,2) DEFAULT NULL,
  `Energy_consumption_intensity` decimal(10,2) DEFAULT NULL,
  `Waste_generated` decimal(10,2) DEFAULT NULL,
  `Water_intensity` decimal(10,2) DEFAULT NULL,
  `Board_independence` tinyint(1) DEFAULT NULL,
  `Women_in_management_team` int DEFAULT NULL,
  `Women_on_board` int DEFAULT NULL,
  `Employees_covered_by_health_insurance` decimal(5,2) DEFAULT NULL,
  `Company_donated` decimal(10,2) DEFAULT NULL,
  `Avg_training_hours_per_employee` decimal(5,2) DEFAULT NULL,
  `Employees_above_50` int DEFAULT NULL,
  `Female_employees` int DEFAULT NULL,
  `Employee_satisfaction_rate` decimal(5,2) DEFAULT NULL,
  `New_hires_female` int DEFAULT NULL,
  `New_hires_above_50` int DEFAULT NULL,
  `Total_turnover` int DEFAULT NULL,
  `Turnover_female` int DEFAULT NULL,
  `Turnover_above_50` int DEFAULT NULL,
  `Fatalities` int DEFAULT NULL,
  `High_consequence_injuries` int DEFAULT NULL,
  `Work_related_injuries` int DEFAULT NULL,
  PRIMARY KEY (`score_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ESG_Scores`
--

LOCK TABLES `ESG_Scores` WRITE;
/*!40000 ALTER TABLE `ESG_Scores` DISABLE KEYS */;
INSERT INTO `ESG_Scores` VALUES (1,1,'AEM',72.33,'AA',29.88,30.37,12.07,100.00,100.00,75.00,0.00,0,0,0,0.00,0.00,75.00,0,0,0.00,0,0,50,0,0,100,100,100),(2,1,'AEM',72.33,'AA',29.88,30.37,12.07,100.00,100.00,75.00,0.00,0,0,0,0.00,0.00,75.00,0,0,0.00,0,0,50,0,0,100,100,100),(3,1,'AEM',72.33,'AA',29.88,30.37,12.07,100.00,100.00,75.00,0.00,0,0,0,0.00,0.00,75.00,0,0,0.00,0,0,50,0,0,100,100,100),(4,1,'AEM',72.33,'AA',29.88,30.37,12.07,100.00,100.00,75.00,0.00,0,0,0,0.00,0.00,75.00,0,0,0.00,0,0,50,0,0,100,100,100),(5,2,'OUEH',70.77,'A',28.76,26.13,15.87,100.00,100.00,0.00,0.00,0,100,0,0.00,0.00,0.00,0,0,0.00,0,0,50,0,0,100,100,100),(6,3,'RMG',65.81,'A',24.22,26.78,14.81,0.00,100.00,0.00,0.00,0,50,25,0.00,100.00,25.00,0,0,0.00,0,0,50,0,0,100,100,100),(7,4,'iXBiopharma',57.99,'A',27.57,18.33,12.09,100.00,100.00,100.00,0.00,0,0,25,0.00,0.00,100.00,0,0,0.00,0,0,0,0,0,100,100,100),(8,5,'AML',57.99,'A',21.09,24.78,12.13,100.00,100.00,0.00,0.00,0,0,75,0.00,0.00,0.00,0,0,0.00,0,0,100,0,0,100,100,100),(9,6,'TGL',56.05,'BBB',16.84,33.17,6.04,100.00,0.00,0.00,0.00,0,0,0,0.00,0.00,100.00,0,0,0.00,0,0,100,0,0,100,100,100),(10,7,'TopGlove',50.84,'BBB',27.50,15.35,7.99,100.00,75.00,100.00,0.00,0,50,75,0.00,75.00,100.00,0,0,0.00,0,0,0,0,0,100,100,100),(11,8,'Abbott',49.98,'BBB',16.54,17.10,16.34,100.00,100.00,0.00,0.00,0,50,75,0.00,0.00,0.00,0,0,0.00,0,0,100,0,0,100,0,0),(12,9,'UGHC',47.21,'BBB',25.07,8.16,13.97,50.00,75.00,0.00,0.00,0,50,0,0.00,0.00,25.00,0,0,0.00,0,0,0,0,0,100,100,0),(13,10,'Medtecs',45.96,'BBB',27.50,5.14,13.32,100.00,100.00,100.00,0.00,50,0,75,50.00,0.00,0.00,0,0,0.00,0,0,0,0,0,0,0,0),(14,11,'Setsco Services',39.75,'BB',14.46,15.58,9.71,100.00,100.00,75.00,0.00,50,25,50,0.00,0.00,25.00,0,0,0.00,0,0,0,0,0,100,100,50),(15,12,'Haw Par',28.76,'BB',5.81,8.57,14.38,0.00,0.00,0.00,0.00,0,0,0,0.00,0.00,0.00,0,0,0.00,0,0,0,0,0,100,0,0),(16,3,'NUS',40.13,'BB',16.92,14.68,8.53,0.00,0.00,0.00,100.00,25,0,0,0.00,0.00,100.00,0,0,0.00,0,0,100,0,0,0,0,100),(17,4,'abc',40.90,'BB',16.92,15.45,8.53,0.00,0.00,0.00,100.00,25,0,0,0.00,0.00,100.00,0,0,0.00,0,50,100,0,0,0,0,100);
/*!40000 ALTER TABLE `ESG_Scores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Firm`
--

DROP TABLE IF EXISTS `Firm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Firm` (
  `firm_name` varchar(50) NOT NULL,
  `industry` varchar(100) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  UNIQUE KEY `firm_name` (`firm_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Firm`
--

LOCK TABLES `Firm` WRITE;
/*!40000 ALTER TABLE `Firm` DISABLE KEYS */;
INSERT INTO `Firm` VALUES ('111','Real Estate','Singapore','https://investors.aem.com.sg'),('abc','Industrials','Singapore','https://investors.aem.com.sg'),('AEM','Consumer Discretionary','Singapore','https://investors.aem.com.sg'),('avb','Financial','Singapore','https://investors.aem.com.sg'),('Mac','Industrials','Singapore','https://investors.aem.com.sg'),('NUS','Industrials','Singapore','https://investors.aem.com.sg'),('R','Health Care','Singapore','https://investors.aem.com.sg');
/*!40000 ALTER TABLE `Firm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Structured_data`
--

DROP TABLE IF EXISTS `Structured_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Structured_data` (
  `data_id` int NOT NULL AUTO_INCREMENT,
  `company_name` varchar(255) NOT NULL,
  `metric` varchar(255) NOT NULL,
  `value` decimal(10,2) DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `similiarity` decimal(10,2) DEFAULT NULL,
  `confidence` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`data_id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Structured_data`
--

LOCK TABLES `Structured_data` WRITE;
/*!40000 ALTER TABLE `Structured_data` DISABLE KEYS */;
INSERT INTO `Structured_data` VALUES (1,'NUS','Absolute_emissions',1.00,NULL,'2024-11-13 04:44:30',0.94,0.80),(2,'NUS','Anti_corruption_disclosures',1.00,'incidents','2024-11-13 04:44:30',0.90,0.95),(3,'NUS','Assurance_of_sustainability_report',1.00,NULL,'2024-11-13 04:44:30',0.92,0.98),(4,'NUS','Average_training_hours_per_employee',480.00,'hours','2024-11-13 04:44:30',0.94,0.90),(5,'NUS','Board_independence',40.00,'%','2024-11-13 04:44:30',0.95,0.95),(6,'NUS','Consumer_rights_protection',1.00,NULL,'2024-11-13 04:44:30',0.92,0.00),(7,'NUS','Current_employees_by_age_groups',80.00,'%','2024-11-13 04:44:30',0.95,0.90),(8,'NUS','Energy_consumption_intensity',29.00,'%','2024-11-13 04:44:30',0.93,0.85),(9,'NUS','Green_financing_projects',1.00,'tonnes CO2e / revenue S$ 000','2024-11-13 04:44:30',0.88,0.95),(10,'NUS','Philanthropic_initiatives',1.00,'%','2024-11-13 04:44:30',0.90,0.90),(11,'NUS','Total_energy_consumption',1.00,NULL,'2024-11-13 04:44:30',0.92,0.99),(12,'NUS','Total_number_of_employees',376.00,'hours','2024-11-13 04:44:30',0.91,0.90),(13,'NUS','Total_turnover',13.70,'%','2024-11-13 04:44:30',0.98,0.90),(14,'NUS','Turnover_by_age',66.00,'%','2024-11-13 04:44:30',0.94,0.90),(15,'NUS','Water_consumption',830232.00,'kWh','2024-11-13 04:44:30',0.94,0.95),(16,'NUS','Water_intensity',0.04,'kWh / revenue S$ 000','2024-11-13 04:44:30',0.98,0.95),(17,'NUS','Work_related_injuries',0.00,'incidents','2024-11-13 04:44:30',0.91,0.95),(18,'abc','Absolute_emissions',1.00,NULL,'2024-11-13 04:51:28',0.94,0.80),(19,'abc','Anti_corruption_disclosures',1.00,'incidents','2024-11-13 04:51:28',0.90,0.95),(20,'abc','Assurance_of_sustainability_report',1.00,NULL,'2024-11-13 04:51:28',0.92,0.98),(21,'abc','Average_training_hours_per_employee',480.00,'hours','2024-11-13 04:51:28',0.94,0.90),(22,'abc','Board_independence',40.00,'%','2024-11-13 04:51:28',0.95,0.95),(23,'abc','Consumer_rights_protection',1.00,'complaints','2024-11-13 04:51:28',0.89,0.90),(24,'abc','Current_employees_by_age_groups',80.00,'%','2024-11-13 04:51:28',0.95,0.90),(25,'abc','Current_employees_by_gender',10.10,'%','2024-11-13 04:51:28',0.90,0.90),(26,'abc','Energy_consumption_intensity',29.00,'%','2024-11-13 04:51:28',0.93,0.90),(27,'abc','Green_financing_projects',1.00,'tonnes CO2e / revenue S$ 000','2024-11-13 04:51:28',0.88,0.95),(28,'abc','New_hires_by_age',6.50,'%','2024-11-13 04:51:28',0.91,0.90),(29,'abc','Philanthropic_initiatives',1.00,'%','2024-11-13 04:51:28',0.90,0.95),(30,'abc','Total_energy_consumption',1.00,NULL,'2024-11-13 04:51:28',0.92,0.99),(31,'abc','Total_number_of_employees',376.00,'hours','2024-11-13 04:51:28',0.91,0.90),(32,'abc','Total_turnover',13.70,'%','2024-11-13 04:51:28',0.98,0.90),(33,'abc','Turnover_by_age',66.00,'%','2024-11-13 04:51:28',0.94,0.90),(34,'abc','Water_consumption',830232.00,'kWh','2024-11-13 04:51:28',0.94,0.95),(35,'abc','Water_intensity',0.04,'kWh / revenue S$ 000','2024-11-13 04:51:28',0.98,0.95),(36,'abc','Work_related_injuries',0.00,'incidents','2024-11-13 04:51:28',0.91,0.95);
/*!40000 ALTER TABLE `Structured_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `role` enum('person','firm','regulator') NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'andrew96','XMSu5nXE@7#z','41922516','firm'),(2,'andrew40','xkELoy!4Rc8+','15764783','firm'),(3,'coryrasmussen','^3xnxxoE0DlS','46882016','firm'),(4,'singletontammy','52&2KBIzfZ1Z','17643226','regulator'),(5,'mwalters','iz3nXs7q_#eY','59445204','firm'),(6,'alexis66','vMB5#U0eOq)L','67898384','regulator'),(7,'jonathanjohnson','5nuKp$fN+R9u','94986919','firm'),(8,'melissakelly','$^G7Xa1haG+n','85905553','firm'),(9,'devin52','#g63FpvJb8ez','55561650','firm'),(10,'lindsey27','#14YhJfkTfW%','98310222','firm'),(11,'cochranwanda','!cZPyRga13g*','92602330','regulator'),(12,'angelaewing','i7^wY!bG#x*A','62028086','regulator'),(13,'coreymorgan','&u#0F)jjBuxI','96814489','person'),(14,'vcisneros','JLy4F8tz@WY$','45855588','firm'),(15,'cabreraleslie','^8Y0wkrGDprN','57373839','person'),(16,'joseph82','E(9&TNwg5T0r','63763735','firm'),(17,'martinderek','&)HaUb_@6V6p','16921800','regulator'),(18,'lucas27','0G*5t7Ej%Mp_','61302091','person'),(19,'sstephenson','BMmSCPVx&W5i','67857811','regulator'),(20,'kevin09','L%+G2B6kPU2A','63611440','regulator'),(21,'phillipcopeland','evS0F6Ab__tw','81864928','firm'),(22,'preed','+4BpURWl4J@o','83018859','person'),(23,'lsingh','cqaFi6pMT^6Z','54733165','person'),(24,'sblake','$1qg$HuhYxBO','33896123','regulator'),(25,'christinagaines','&U7benC17yZS','63904996','firm'),(26,'caitlin28','*z67GM2nvh!J','83537483','regulator'),(27,'rollinsmarcia','p)7buCCiy4R1','67625174','regulator'),(28,'dbell','DNrPI8Dz9Mp#','83436004','firm'),(29,'ccollins','9_(LVVBOci93','36313993','firm'),(30,'williamsernest','(tYtpmh(08@I','12963574','firm'),(31,'qadams','B*b5hiLl#v^Z','27015181','firm'),(32,'yfowler','^f@6ORo8%^1r','80057790','firm'),(33,'ihamilton','TFi4Z3nx#*fF','78141573','person'),(34,'paynelisa',')Dp3Me@waIRZ','36335290','person'),(35,'thall','$1#GDgnD$9&)','54324194','regulator'),(36,'debra06','%7tLzCRPigJ9','70335899','person'),(37,'pjackson','xpD%O&vV&&9r','26515372','firm'),(38,'jamesturner','(!Q+2VxngXF)','37677573','person'),(39,'chavezkimberly','AB0kJa@k@3On','73094153','regulator'),(40,'millsphillip','*)dRJp!7q*30','56702400','person'),(41,'fowlerlinda',')In4QCvC!6zt','35684237','firm'),(42,'hhoward','OzcR3Vru+^fP','49326371','firm'),(43,'jenniferjones','4X9R6c5jE!WV','17542742','firm'),(44,'ashleyjohnson','!(nA8LlSpP4b','16228081','regulator'),(45,'williamrose','jD2lMxKkm4@A','20536854','person'),(46,'crystalhenson','#zU)VzVD4@Sq','51400810','regulator'),(47,'jennasmith','^5L)ew+(RZCY','80173731','person'),(48,'john65','y*1+SSk440Sn','86787044','person'),(49,'lindsay40','^5HdibjQ@1Ot','45519427','firm'),(50,'bakerjustin','X4jD#fwq^4uP','12587107','regulator'),(51,'alvarezchristopher','(pE6XEgn2Y$J','54713603','regulator'),(52,'millermichelle','uws6mitw)3YR','81319243','person'),(53,'eboyd','2dx^o3XYq9Q(','76434903','firm'),(54,'donna19','(0^Cg2Td^t1J','35052340','firm'),(55,'zimmermanlaura','C_%G2O$Y@9Le','95835969','firm'),(56,'lindaconley','XH!RoneT^7zk','45548034','firm'),(57,'lroberts','L2SuSs1x!1L2','16226649','firm'),(58,'tparks','06&&Swua(qus','22938142','firm'),(59,'jacobskenneth','$3#v^Dyp3J@T','40879054','person'),(60,'melissasantos','(9eci%mI_QK@','81194821','regulator'),(61,'swright','_mV2m3ceW4AB','89342052','firm'),(62,'psmith','0QC6UJ+u%Y)w','30063690','firm'),(63,'stephen35','$oj1O2zs0ZWy','25048266','firm'),(64,'kelli72','La8Q5XVxX&ex','49910244','person'),(65,'jacqueline01','dV1fDRf*)z70','35378374','firm'),(66,'amanda57','+pQ3dHsh+Ef3','74240543','firm'),(67,'dacosta','xL+6Of*(ITc*','63794912','firm'),(68,'uerickson','Hh53q#Wx#$9K','95407269','firm'),(69,'amy92','!L80*Qyoh#4P','78391970','firm'),(70,'wschneider','49EWz9Ea!)3z','62983057','firm'),(71,'riosjohn','5%7VLj$(6&Gm','44084787','firm'),(72,'ybenton','DuVYedZP)4EZ','76129584','person'),(73,'andreasoto','#yciAPZJw2Pc','93504313','firm'),(74,'kendrabarry','&Y5Jz#dj96q^','23688572','firm'),(75,'jimmymcdonald','i*24)NOtGNx1','53386780','firm'),(76,'carsonkimberly','V!14PJrBEEUR','81903834','firm'),(77,'james93','i@o8D@e2Iavq','87306216','firm'),(78,'jfinley','7pftwl+O_U)K','57870460','regulator'),(79,'kfletcher','%2AWHTjsLP8d','67598282','person'),(80,'jenkinsjohn','dOVa6$vlU#6j','64259031','regulator'),(81,'perezjoshua','M_59Mtp(%80C','54319612','person'),(82,'robin42','wL9Jy%tj$CHT','83991784','regulator'),(83,'greendiana','x@Rcoqz&(4nf','59458898','regulator'),(84,'alexanderchristina','8D_4Q%jmplnm','10775494','person'),(85,'aguilarjacob','l6@6WX*bGAqe','69573426','firm'),(86,'wcarter','5(mBN(PaXB8C','92603718','firm'),(87,'danny50','P40RFp7Vdz)^','50556788','firm'),(88,'sarahkim','(i3DjF9dhpXo','10037804','person'),(89,'kaitlyn87','p$0sV2CyW&jr','90855041','firm'),(90,'xward','$kuIJCb_i9T3','64660166','firm'),(91,'curtisbeth','!^p($7Vjw1Di','37134328','person'),(92,'iperez','S%0NSc9h*R8@','96382336','firm'),(93,'melissa70','+kOyrSbo$96I','44462903','firm'),(94,'shaas',')F7WEUfV2eBL','52703703','firm'),(95,'wryan','k4OkZ$(i)vX&','51831441','firm'),(96,'patricktucker','#bf@2Ip$e*T%','62189202','regulator'),(97,'brittany49','6_7hU5Xf^AY&','38595001','person'),(98,'garybrooks','@S1Zjhh#(%S$','82215715','firm'),(99,'rodney00','3WY^pfiM$ueI','92265028','firm'),(100,'nryan','+T2krzsrV0Dm','17246812','firm'),(102,'bcd','1111','12345678','person'),(103,'sxy','111','12345678','person'),(104,'a1','111','12345678','firm'),(105,'bb','111','111','regulator'),(106,'aa','111','1111','regulator'),(107,'qq','111','111','regulator');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-13 12:54:53
