/*
Navicat MySQL Data Transfer

Source Server         : con
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : cloudlesson

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2016-07-09 20:39:41
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `course_id` varchar(100) NOT NULL,
  `url` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES ('1', '程序设计入门—Java语言', 'ZJU-1000002014', 'http://mooc.study.163.com/course/ZJU-1000002014');
INSERT INTO `course` VALUES ('2', 'Java语言程序设计进阶', 'ZJU-1000004001', 'http://mooc.study.163.com/course/ZJU-1000004001');
INSERT INTO `course` VALUES ('3', '程序设计入门—C语言', 'ZJU-1000002011', 'http://mooc.study.163.com/course/ZJU-1000002011');
INSERT INTO `course` VALUES ('4', 'C语言程序设计进阶', 'ZJU-1000004000', 'http://mooc.study.163.com/course/ZJU-1000004000');
INSERT INTO `course` VALUES ('5', '程序设计入门—Python', 'HIT-1000002017', 'http://mooc.study.163.com/course/HIT-1000002017');
INSERT INTO `course` VALUES ('6', '计算机专业导论', 'hit-437006', 'http://www.icourse163.org/course/hit-437006');
INSERT INTO `course` VALUES ('7', '计算机专业导论之思维与系统', 'HIT-1000003008', 'http://mooc.study.163.com/course/HIT-1000003008');
INSERT INTO `course` VALUES ('8', '计算机专业导论之语言与算法', 'HIT-1000004007', 'http://mooc.study.163.com/course/HIT-1000004007');
INSERT INTO `course` VALUES ('9', '计算机专业导论之学科与专业', 'HIT-1000004008', 'http://mooc.study.163.com/course/HIT-1000004008');
INSERT INTO `course` VALUES ('10', '工科数学分析（一）', 'hit-153001', 'http://www.icourse163.org/course/hit-153001');
INSERT INTO `course` VALUES ('11', '工科数学分析（二）', 'hit-207002', 'http://www.icourse163.org/course/hit-207002');
INSERT INTO `course` VALUES ('12', 'C++程序设计入门(上)', 'BUPT-1000003015', 'http://mooc.study.163.com/course/BUPT-1000003015');
INSERT INTO `course` VALUES ('13', 'C++程序设计入门(下)', 'BUPT-1000005002', 'http://mooc.study.163.com/course/BUPT-1000005002');
INSERT INTO `course` VALUES ('14', '数据结构', 'ZJU-1000033001', 'http://mooc.study.163.com/course/ZJU-1000033001');
INSERT INTO `course` VALUES ('15', 'C#程序设计(上)', 'PKU-1000003003', 'http://mooc.study.163.com/course/PKU-1000003003');
INSERT INTO `course` VALUES ('16', 'C#程序设计(下)', 'PKU-1000003006', 'http://mooc.study.163.com/course/PKU-1000003006');
INSERT INTO `course` VALUES ('17', '计算机组成原理之机器', 'HIT-1000002002', 'http://mooc.study.163.com/course/HIT-1000002002');
INSERT INTO `course` VALUES ('18', '计算机组成原理之数字', 'HIT-1000003000', 'http://mooc.study.163.com/course/HIT-1000003000');
INSERT INTO `course` VALUES ('19', '计算机组成原理之CPU', 'HIT-1000002003', 'http://mooc.study.163.com/course/HIT-1000002003');
INSERT INTO `course` VALUES ('20', '算法设计与分析之入门篇', 'HIT-1000002012', 'http://mooc.study.163.com/course/HIT-1000002012');
INSERT INTO `course` VALUES ('21', '算法设计与分析之进阶篇', 'HIT-1000005000', 'http://mooc.study.163.com/course/HIT-1000005000');
INSERT INTO `course` VALUES ('22', '算法设计与分析之高级篇', 'HIT-1000004002', 'http://mooc.study.163.com/course/HIT-1000004002');
INSERT INTO `course` VALUES ('23', '算法设计与分析之随机算法篇', 'HIT-1000004003', 'http://mooc.study.163.com/course/HIT-1000004003');
INSERT INTO `course` VALUES ('24', '算法设计与分析之近似算法篇', 'HIT-1000005001', 'http://mooc.study.163.com/course/HIT-1000005001');
INSERT INTO `course` VALUES ('25', '算法设计与分析之大数据算法篇', 'HIT-1000004006', 'http://mooc.study.163.com/course/HIT-1000004006');
INSERT INTO `course` VALUES ('26', '算法设计与分析专题之计算几何篇', 'HIT-1000004004', 'http://mooc.study.163.com/course/HIT-1000004004');
INSERT INTO `course` VALUES ('27', '算法设计与分析专题之组合优化篇', 'HIT-1000004005', 'http://mooc.study.163.com/course/HIT-1000004005');
INSERT INTO `course` VALUES ('28', '离散数学基础', 'SYSU-1000002018', 'http://mooc.study.163.com/course/SYSU-1000002018');
INSERT INTO `course` VALUES ('29', '概率论与数理统计', 'NJU-1000031001', 'http://mooc.study.163.com/course/NJU-1000031001');
INSERT INTO `course` VALUES ('30', '软件工程（C编码实践篇）', 'USTC-1000002006', 'http://mooc.study.163.com/course/USTC-1000002006');
INSERT INTO `course` VALUES ('31', '软件工程（OO分析与设计篇）', 'USTC-1000003012', 'http://mooc.study.163.com/course/USTC-1000003012');
INSERT INTO `course` VALUES ('32', '软件工程（过程与管理篇）', 'USTC-1000003013', 'http://mooc.study.163.com/course/USTC-1000003013');
INSERT INTO `course` VALUES ('33', '编译原理', 'USTC-1000002001', 'http://mooc.study.163.com/course/USTC-1000002001');
INSERT INTO `course` VALUES ('34', '操作系统之基础', 'HIT-1000002004', 'http://mooc.study.163.com/course/HIT-1000002004');
INSERT INTO `course` VALUES ('35', '操作系统之进程与线程', 'HIT-1000002008', 'http://mooc.study.163.com/course/HIT-1000002008');
INSERT INTO `course` VALUES ('36', '操作系统之内存管理', 'HIT-1000003007', 'http://mooc.study.163.com/course/HIT-1000003007');
INSERT INTO `course` VALUES ('37', '操作系统之外设与文件系统', 'HIT-1000002009', 'http://mooc.study.163.com/course/HIT-1000002009');
INSERT INTO `course` VALUES ('38', '计算机网络之网尽其用', 'HIT-1000002010', 'http://mooc.study.163.com/course/HIT-1000002010');
INSERT INTO `course` VALUES ('39', '计算机网络之探赜索隐', 'HIT-1000004012', 'http://mooc.study.163.com/course/HIT-1000004012');
INSERT INTO `course` VALUES ('40', '计算机网络之危机四伏', 'HIT-1000005009', 'http://mooc.study.163.com/course/HIT-1000005009');
INSERT INTO `course` VALUES ('41', '计算机网络之基础链路', 'SYSU-1000003010', 'http://mooc.study.163.com/course/SYSU-1000003010');
INSERT INTO `course` VALUES ('42', '计算机网络之构造互联网', 'SYSU-1000002015', 'http://mooc.study.163.com/course/SYSU-1000002015');
INSERT INTO `course` VALUES ('43', '计算机网络之高阶应用', 'SYSU-1000003011', 'http://mooc.study.163.com/course/SYSU-1000003011');
INSERT INTO `course` VALUES ('44', '数据库系统原理', 'ZJU-1000031000', 'http://mooc.study.163.com/course/ZJU-1000031000');
INSERT INTO `course` VALUES ('45', '数据库系统（上）', 'hit-1001516002', 'http://www.icourse163.org/course/hit-1001516002');
INSERT INTO `course` VALUES ('46', '数据库系统（中）', 'hit-1001554030', 'http://www.icourse163.org/course/hit-1001554030');
INSERT INTO `course` VALUES ('47', '数据库系统（下）', 'hit-1001578001', 'http://www.icourse163.org/course/hit-1001578001');
INSERT INTO `course` VALUES ('48', '线性代数', 'sdu-55001', 'http://www.icourse163.org/course/sdu-55001');
INSERT INTO `course` VALUES ('49', '软件测试', 'NJU-1000122000', 'http://mooc.study.163.com/course/NJU-1000122000');
INSERT INTO `course` VALUES ('50', '软件测试方法和技术实践', 'Tongji-1000002019', 'http://mooc.study.163.com/course/Tongji-1000002019');
INSERT INTO `course` VALUES ('51', '面向对象软件开发实践之基本技能训练', 'BIT-1000003016', 'http://mooc.study.163.com/course/BIT-1000003016');
INSERT INTO `course` VALUES ('52', '面向对象软件开发实践之专业技能训练', 'BIT-1000013000', 'http://mooc.study.163.com/course/BIT-1000013000');
INSERT INTO `course` VALUES ('53', '面向对象软件开发实践之实战技能训练', 'BIT-1000013001', 'http://mooc.study.163.com/course/BIT-1000013001');
INSERT INTO `course` VALUES ('54', '计算机系统结构 (一) 基本概念及指令集', 'BUPT-1000002016', 'http://mooc.study.163.com/course/BUPT-1000002016');
INSERT INTO `course` VALUES ('55', '计算机系统结构 (二) 计算机主要系统构成', 'BUPT-1000005004', 'http://mooc.study.163.com/course/BUPT-1000005004');
INSERT INTO `course` VALUES ('56', '计算机系统结构 (三) CPU及其结构分析', 'BUPT-1000005005', 'http://mooc.study.163.com/course/BUPT-1000005005');
INSERT INTO `course` VALUES ('57', 'Linux内核分析', 'USTC-1000029000', 'http://mooc.study.163.com/course/USTC-1000029000');
INSERT INTO `course` VALUES ('58', '软件安全之恶意代码机理与防护', 'WHU-1000003014', 'http://mooc.study.163.com/course/WHU-1000003014');
INSERT INTO `course` VALUES ('59', '软件安全之软件漏洞机理与防护', 'WHU-1000032000', 'http://mooc.study.163.com/course/WHU-1000032000');
INSERT INTO `course` VALUES ('60', '信息安全数学基础', 'HIT-1000002013', 'http://mooc.study.163.com/course/HIT-1000002013');
INSERT INTO `course` VALUES ('61', '近世代数', 'HIT-1000003009', 'http://mooc.study.163.com/course/HIT-1000003009');
