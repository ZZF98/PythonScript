/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80017
 Source Host           : localhost:3306
 Source Schema         : video_data

 Target Server Type    : MySQL
 Target Server Version : 80017
 File Encoding         : 65001

 Date: 23/09/2019 20:07:17
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for video_data
-- ----------------------------
DROP TABLE IF EXISTS `video_data`;
CREATE TABLE `video_data`  (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `device_serial` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '设备序列号',
  `clinic_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '诊所名',
  `start_date` datetime(0) NULL DEFAULT NULL COMMENT '开始时间',
  `date` bigint(128) NULL DEFAULT NULL COMMENT '日期',
  `file_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '文件名',
  `status` tinyint(2) NULL DEFAULT NULL COMMENT '状态',
  `url` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '上传文件地址',
  `new_file_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '新文件名',
  `file_id` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '图片id',
  `end_date` datetime(0) NULL DEFAULT NULL COMMENT '结束时间',
  `file_size` double(64, 0) NULL DEFAULT NULL COMMENT '文件大小',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9112 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
