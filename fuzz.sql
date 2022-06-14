-- MySQL dump 10.13  Distrib 5.7.38, for Linux (x86_64)
--
-- Host: localhost    Database: fuzz
-- ------------------------------------------------------
-- Server version	5.7.38-0ubuntu0.18.04.1

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
-- Table structure for table `crashes`
--

DROP TABLE IF EXISTS `crashes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crashes` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `name` char(60) DEFAULT NULL,
  `jobid` int(20) DEFAULT NULL,
  `crashpath` char(100) DEFAULT NULL,
  `isfix` int(11) DEFAULT NULL,
  `findtime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1009 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crashes`
--

LOCK TABLES `crashes` WRITE;
/*!40000 ALTER TABLE `crashes` DISABLE KEYS */;
INSERT INTO `crashes` VALUES (970,'7984654_ybxm-linux-A1_info_2',54,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/7984654/crashs',0,'2022-02-25 21:44:37'),(971,'honggfuzz-test_ybxm-linux-A1_info_31',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(972,'honggfuzz-test_ybxm-linux-A1_info_23',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(973,'honggfuzz-test_ybxm-linux-A1_info_42',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(974,'honggfuzz-test_ybxm-linux-A1_info_4',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(975,'honggfuzz-test_ybxm-linux-A1_info_44',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(976,'honggfuzz-test_ybxm-linux-A1_info_8',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(977,'honggfuzz-test_ybxm-linux-A1_info_0',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(978,'honggfuzz-test_ybxm-linux-A1_info_1',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(979,'honggfuzz-test_ybxm-linux-A1_info_9',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(980,'honggfuzz-test_ybxm-linux-A1_info_21',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(981,'honggfuzz-test_ybxm-linux-A1_info_30',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:27'),(982,'honggfuzz-test_ybxm-linux-A1_info_43',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(983,'honggfuzz-test_ybxm-linux-A1_info_35',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(984,'honggfuzz-test_ybxm-linux-A1_info_18',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(985,'honggfuzz-test_ybxm-linux-A1_info_33',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(986,'honggfuzz-test_ybxm-linux-A1_info_28',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(987,'honggfuzz-test_ybxm-linux-A1_info_45',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(988,'honggfuzz-test_ybxm-linux-A1_info_26',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(989,'honggfuzz-test_ybxm-linux-A1_info_29',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(990,'honggfuzz-test_ybxm-linux-A1_info_16',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(991,'honggfuzz-test_ybxm-linux-A1_info_37',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(992,'honggfuzz-test_ybxm-linux-A1_info_22',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(993,'honggfuzz-test_ybxm-linux-A1_info_3',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(994,'honggfuzz-test_ybxm-linux-A1_info_14',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(995,'honggfuzz-test_ybxm-linux-A1_info_38',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(996,'honggfuzz-test_ybxm-linux-A1_info_17',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(997,'honggfuzz-test_ybxm-linux-A1_info_6',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(998,'honggfuzz-test_ybxm-linux-A1_info_20',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(999,'honggfuzz-test_ybxm-linux-A1_info_41',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(1000,'honggfuzz-test_ybxm-linux-A1_info_13',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(1001,'honggfuzz-test_ybxm-linux-A1_info_12',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(1002,'honggfuzz-test_ybxm-linux-A1_info_25',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(1003,'honggfuzz-test_ybxm-linux-A1_info_11',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(1004,'honggfuzz-test_ybxm-linux-A1_info_40',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(1005,'honggfuzz-test_ybxm-linux-A1_info_36',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(1006,'honggfuzz-test_ybxm-linux-A1_info_27',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(1007,'honggfuzz-test_ybxm-linux-A1_info_15',57,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test/crashs',0,'2022-02-26 21:39:28'),(1008,'openssl-libfuzz_ybxm-linux-A1_info_5',62,'/home/ybxm/myClusterFuzz/MyServer/jobprojects/openssl-libfuzz/crashs',0,'2022-03-10 09:32:47');
/*!40000 ALTER TABLE `crashes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `name` char(30) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `fuzzer` char(100) DEFAULT NULL,
  `botnum` int(11) DEFAULT NULL,
  `surplusnum` int(11) DEFAULT NULL COMMENT '任务剩余数',
  `completenum` int(11) DEFAULT NULL COMMENT '任务完成度',
  `time` int(11) DEFAULT NULL,
  `exec` char(100) DEFAULT NULL,
  `jobpath` char(100) DEFAULT NULL,
  `crashnum` int(11) DEFAULT NULL,
  `createtime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (53,'96320',1,'AFL',1,0,1,60,'test_asan','/home/ybxm/myClusterFuzz/MyServer/jobprojects/96320',0,'2022-02-25 21:38:29'),(54,'7984654',1,'Libfuzz',1,0,1,60,'handshake-fuzzer','/home/ybxm/myClusterFuzz/MyServer/jobprojects/7984654',1,'2022-02-25 21:43:04'),(56,'266',1,'AFLFAST',1,0,1,60,'test_asan','/home/ybxm/myClusterFuzz/MyServer/jobprojects/266',0,'2022-02-26 16:12:27'),(57,'honggfuzz-test',1,'Honggfuzz',1,0,1,60,'badcode1','/home/ybxm/myClusterFuzz/MyServer/jobprojects/honggfuzz-test',37,'2022-02-26 21:37:48'),(58,'27-afl',1,'AFL',1,0,1,60,'test_asan','/home/ybxm/myClusterFuzz/MyServer/jobprojects/27-afl',0,'2022-02-27 14:29:05'),(59,'27-Integer-test',2,'AFL+AFLFAST+Libfuzz+Honggfuzz',4,0,4,60,'sqlite3AFL+sqliteAFLFAST+sqliteLibfuzz+sqlite3Honggfuzz','/home/ybxm/myClusterFuzz/MyServer/jobprojects/27-Integer-test',0,'2022-02-27 14:35:14'),(61,'27-integer-3',2,'AFL+AFLFAST+Libfuzz+Honggfuzz',4,0,4,60,'sqlite3AFL+sqliteAFLFAST+sqliteLibfuzz+sqlite3Honggfuzz','/home/ybxm/myClusterFuzz/MyServer/jobprojects/27-integer-3',0,'2022-02-27 16:35:53'),(62,'openssl-libfuzz',1,'Libfuzz',1,0,1,60,'handshake-fuzzer','/home/ybxm/myClusterFuzz/MyServer/jobprojects/openssl-libfuzz',1,'2022-03-10 09:31:16'),(63,'test-6-10',1,'FairFuzz',1,0,1,60,'test_asan','/home/ybxm/myClusterFuzz/MyServer/jobprojects/test-6-10',0,'2022-06-10 20:59:00'),(64,'test-radamsa',1,'Radamsa',1,0,1,60,'cflow','/home/ybxm/myClusterFuzz/MyServer/jobprojects/test-radamsa',0,'2022-06-10 21:05:32'),(65,'test-6-11',3,'AFLFAST+QSYM',3,3,0,30,'cflow','/home/ybxm/myClusterFuzz/MyServer/jobprojects/test-6-11',0,'2022-06-11 17:28:27'),(66,'123546',2,'AFL+AFLFAST+Libfuzz+Radamsa',4,4,0,20,'cflow','/home/ybxm/myClusterFuzz/MyServer/jobprojects/123546',0,'2022-06-11 18:01:51'),(67,'aflgo-test',4,'ALFGO',1,1,0,30,'cflow','/home/ybxm/myClusterFuzz/MyServer/jobprojects/aflgo-test',0,'2022-06-11 18:07:36');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nodes`
--

DROP TABLE IF EXISTS `nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(20) DEFAULT NULL,
  `ipaddr` char(20) DEFAULT NULL,
  `men` int(11) DEFAULT NULL,
  `corenum` int(11) DEFAULT NULL,
  `jobid` int(20) DEFAULT NULL,
  `fetchtime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '节点提取任务时间',
  `last_modify_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '最后活跃时间',
  `createtime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nodes`
--

LOCK TABLES `nodes` WRITE;
/*!40000 ALTER TABLE `nodes` DISABLE KEYS */;
INSERT INTO `nodes` VALUES (7,'ybxm-linux-A1','192.168.178.109',15,6,0,'2022-06-10 21:05:39','2022-06-10 21:07:10','2022-02-25 21:25:25'),(8,'ybxm-linux-node1','192.168.178.109',15,6,0,'2022-02-27 16:36:01','2022-02-27 16:37:45','2022-02-27 14:29:12'),(9,'ybxm-linux-node2','192.168.178.109',15,6,0,'2022-02-27 16:36:03','2022-02-27 16:37:46','2022-02-27 16:06:24'),(10,'ybxm-linux-node3','192.168.178.109',15,6,0,'2022-02-27 16:36:06','2022-02-27 16:37:49','2022-02-27 16:06:26');
/*!40000 ALTER TABLE `nodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reproduce`
--

DROP TABLE IF EXISTS `reproduce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reproduce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(20) DEFAULT NULL,
  `fuzzer` char(15) DEFAULT NULL,
  `crashname` char(60) DEFAULT NULL,
  `exec` char(20) DEFAULT NULL,
  `jobpath` varchar(100) DEFAULT NULL,
  `completed` int(11) DEFAULT NULL,
  `isfetch` int(11) DEFAULT NULL,
  `isfixed` int(11) DEFAULT NULL,
  `createtime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reproduce`
--

LOCK TABLES `reproduce` WRITE;
/*!40000 ALTER TABLE `reproduce` DISABLE KEYS */;
INSERT INTO `reproduce` VALUES (13,'openssl-repro','Libfuzz','openssl-libfuzz_ybxm-linux-A1_info_5','handshake-fuzzer','/home/ybxm/myClusterFuzz/MyServer/jobprojects/openssl-repro',1,1,0,'2022-03-10 09:43:08');
/*!40000 ALTER TABLE `reproduce` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-14 16:46:40
