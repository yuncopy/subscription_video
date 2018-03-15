/*
Navicat MySQL Data Transfer

Source Server         : 192.168.4.9
Source Server Version : 50638
Source Host           : 192.168.4.9:3306
Source Database       : movie

Target Server Type    : MYSQL
Target Server Version : 50638
File Encoding         : 65001

Date: 2018-03-14 11:49:36
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `is_super` smallint(6) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_admin_addtime` (`addtime`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('1', 'admin', 'pbkdf2:sha256:50000$rxSlGr9G$81b0329e6236cf1dea80a67f8c85aaf09e4869a61de0f9e01900e6b300e5fdd2', '0', '1', '2018-03-07 15:24:20');
INSERT INTO `admin` VALUES ('2', 'yuncopy', 'pbkdf2:sha256:50000$uT9DtwYw$aff5862f5a94289dc4203beed75c51c3f9982b7ef05b04d8b4c35b2ee0a93a34', '1', '3', '2018-03-12 09:54:15');
INSERT INTO `admin` VALUES ('3', 'yun', 'pbkdf2:sha256:50000$0oqXSnN5$50353a0c0bd6cbfb36bb3cdef3b518cf39f7cfe748d9da800279709626dbd746', '1', '7', '2018-03-12 09:54:37');

-- ----------------------------
-- Table structure for adminlog
-- ----------------------------
DROP TABLE IF EXISTS `adminlog`;
CREATE TABLE `adminlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_adminlog_addtime` (`addtime`),
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of adminlog
-- ----------------------------
INSERT INTO `adminlog` VALUES ('1', '1', '127.0.0.1', '2018-03-08 19:28:18');
INSERT INTO `adminlog` VALUES ('2', '1', '127.0.0.1', '2018-03-08 19:42:32');
INSERT INTO `adminlog` VALUES ('3', '1', '127.0.0.1', '2018-03-08 19:44:03');
INSERT INTO `adminlog` VALUES ('4', '1', '127.0.0.1', '2018-03-10 16:02:25');
INSERT INTO `adminlog` VALUES ('5', '1', '127.0.0.1', '2018-03-10 16:04:22');
INSERT INTO `adminlog` VALUES ('6', '3', '127.0.0.1', '2018-03-12 10:39:55');
INSERT INTO `adminlog` VALUES ('7', '3', '127.0.0.1', '2018-03-12 10:43:07');
INSERT INTO `adminlog` VALUES ('8', '3', '127.0.0.1', '2018-03-12 10:56:29');
INSERT INTO `adminlog` VALUES ('9', '1', '192.168.4.9', '2018-03-14 11:37:31');
INSERT INTO `adminlog` VALUES ('10', '1', '192.168.4.9', '2018-03-14 11:40:37');

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `name_url_idx` (`name`,`url`) USING BTREE,
  KEY `ix_auth_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth
-- ----------------------------
INSERT INTO `auth` VALUES ('18', '后台首页', '/admin/', '2018-03-12 10:22:08');
INSERT INTO `auth` VALUES ('19', '标签编辑页', '/admin/tag/edit/<int:id>/', '2018-03-12 10:22:51');
INSERT INTO `auth` VALUES ('20', '标签列表页', '/admin/tag/list/<int:page>/', '2018-03-12 10:23:28');
INSERT INTO `auth` VALUES ('21', '标签删除页', '/admin/tag/del/<int:id>/', '2018-03-12 10:23:46');
INSERT INTO `auth` VALUES ('22', '电影编辑页', '/admin/movie/edit/<int:id>/', '2018-03-12 10:24:11');
INSERT INTO `auth` VALUES ('23', '电影列表页', '/admin/movie/list/<int:page>/', '2018-03-12 10:24:47');
INSERT INTO `auth` VALUES ('24', '电影删除页', '/admin/movie/del/<int:id>/', '2018-03-12 10:25:02');
INSERT INTO `auth` VALUES ('25', '会员编辑页', '/admin/user/edit/<int:id>/', '2018-03-12 10:25:24');
INSERT INTO `auth` VALUES ('26', '会员列表页', '/admin/user/list/<int:page>/', '2018-03-12 10:25:39');
INSERT INTO `auth` VALUES ('27', '会员删除页', '/admin/user/del/<int:id>/', '2018-03-12 10:25:58');
INSERT INTO `auth` VALUES ('28', '评论编辑页', '/admin/comment/edit/<int:id>/', '2018-03-12 10:26:13');
INSERT INTO `auth` VALUES ('29', '评论列表页', '/admin/comment/list/<int:page>/', '2018-03-12 10:26:28');
INSERT INTO `auth` VALUES ('30', '评论删除页', '/admin/comment/del/<int:id>/', '2018-03-12 10:26:41');
INSERT INTO `auth` VALUES ('31', '角色编辑页', '/admin/role/edit/<int:id>/', '2018-03-12 10:27:08');
INSERT INTO `auth` VALUES ('32', '角色列表页', '/admin/role/list/<int:page>/', '2018-03-12 10:27:35');
INSERT INTO `auth` VALUES ('33', '角色删除页', '/admin/role/del/<int:id>/', '2018-03-12 10:27:49');
INSERT INTO `auth` VALUES ('34', '权限编辑页', '/admin/auth/edit/<int:id>/', '2018-03-12 10:28:13');
INSERT INTO `auth` VALUES ('35', '权限列表页', '/admin/auth/list/<int:page>/', '2018-03-12 10:28:39');
INSERT INTO `auth` VALUES ('36', '权限删除页', '/admin/auth/del/<int:id>/', '2018-03-12 10:28:53');
INSERT INTO `auth` VALUES ('37', '角色权限编辑页', '/admin/role/auth/edit/<int:id>/', '2018-03-12 10:29:07');
INSERT INTO `auth` VALUES ('38', '角色权限列表页', '/admin/role/auth/list/<int:p>/', '2018-03-12 10:29:22');
INSERT INTO `auth` VALUES ('39', '角色权限删除页', '/admin/role/auth/del/<int:id>/', '2018-03-12 10:29:39');
INSERT INTO `auth` VALUES ('40', '管理员编辑页', '/admin/admin/edit/<int:id>/', '2018-03-12 10:29:56');
INSERT INTO `auth` VALUES ('41', '管理员列表页', '/admin/admin/list/<int:page>/', '2018-03-12 10:30:11');
INSERT INTO `auth` VALUES ('42', '管理员删除页', '/admin/admin/del/<int:id>/', '2018-03-12 10:30:24');
INSERT INTO `auth` VALUES ('43', '管理员角色编辑页', '/admin/admin/role/edit/<int:id>/', '2018-03-12 10:30:37');
INSERT INTO `auth` VALUES ('44', '管理员角色列表页', '/admin/admin/role/list/<int:p>/', '2018-03-12 10:30:51');
INSERT INTO `auth` VALUES ('45', '管理员角色删除页', '/admin/admin/role/del/<int:id>/', '2018-03-12 10:31:04');
INSERT INTO `auth` VALUES ('46', '日志列表页', '/admin/oplog/list/<int:page>/', '2018-03-12 10:31:25');
INSERT INTO `auth` VALUES ('47', '修改密码页', '/admin/pwd/', '2018-03-12 10:31:43');
INSERT INTO `auth` VALUES ('48', '权限添加页', '/admin/auth/add/', '2018-03-14 11:41:15');
INSERT INTO `auth` VALUES ('49', '标签添加页', '/admin/tag/add/', '2018-03-14 11:41:59');
INSERT INTO `auth` VALUES ('50', '电影添加页', '/admin/movie/add/', '2018-03-14 11:42:31');
INSERT INTO `auth` VALUES ('51', '预告添加页', '/admin/preview/add/', '2018-03-14 11:44:53');
INSERT INTO `auth` VALUES ('53', '预告列表页', '/admin/preview/list/<int:page>/', '2018-03-14 11:48:00');
INSERT INTO `auth` VALUES ('54', '电影收藏页', '/admin/moviecol/list/<int:page>/', '2018-03-14 11:48:03');

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_addtime` (`addtime`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comment
-- ----------------------------
INSERT INTO `comment` VALUES ('1', '呵呵', '1', '4', '2018-03-22 14:09:38');
INSERT INTO `comment` VALUES ('3', '很好，很好看', '4', '6', '2018-03-10 14:11:10');
INSERT INTO `comment` VALUES ('4', '<p>很牛逼，很好看</p>', '2', '6', '2018-03-13 14:29:16');
INSERT INTO `comment` VALUES ('5', '<p>很牛逼，很好看</p>', '2', '6', '2018-03-13 14:29:26');
INSERT INTO `comment` VALUES ('6', '<p>很牛逼，很好看</p>', '2', '6', '2018-03-13 14:29:36');
INSERT INTO `comment` VALUES ('7', '<p>很好看的，很性感<br/></p>', '2', '6', '2018-03-13 14:31:03');
INSERT INTO `comment` VALUES ('8', '<p>哈哈哈</p>', '2', '6', '2018-03-13 14:53:21');
INSERT INTO `comment` VALUES ('9', '<p>啊哈哈</p>', '1', '6', '2018-03-13 14:57:07');
INSERT INTO `comment` VALUES ('10', '<p><img src=\"http://img.baidu.com/hi/jx2/j_0015.gif\"/><img src=\"http://img.baidu.com/hi/jx2/j_0030.gif\"/></p>', '1', '6', '2018-03-13 14:57:42');
INSERT INTO `comment` VALUES ('11', '<p>哈哈哈</p>', '3', '6', '2018-03-13 15:04:58');
INSERT INTO `comment` VALUES ('12', '<p>嗡嗡嗡</p>', '11', '6', '2018-03-13 19:45:13');

-- ----------------------------
-- Table structure for movie
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `info` text,
  `logo` varchar(255) DEFAULT NULL,
  `star` smallint(6) DEFAULT NULL,
  `playnum` bigint(20) DEFAULT NULL,
  `commentnum` bigint(20) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `logo` (`logo`),
  KEY `tag_id` (`tag_id`),
  KEY `ix_movie_addtime` (`addtime`),
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of movie
-- ----------------------------
INSERT INTO `movie` VALUES ('1', '环太平洋', '20180309153623fae397b0b07a44e5b51b8c71830fdcf0.mp4', '环太平洋', '201803091536234f3d803e8e6d4f878c5e2b3448bcf1a9.png', '5', '48', '2', '1', '中国', '2018-03-29', '120分钟', '2018-03-09 15:36:24');
INSERT INTO `movie` VALUES ('2', '《唐人街探案2》', '2018030915404330d4226c72654a1eb2b6982af038c0ae.mp4', '《唐人街探案2》新春拜年会', '2018030915404313437ceedc8e4fa7bad64dda8d0ea4a4.png', '5', '9', '5', '10', '中国', '2018-03-31', '144分钟', '2018-03-09 15:40:44');
INSERT INTO `movie` VALUES ('3', '《红海行动》发布会', '201803091541371676c14982484b4a98a994f957336dbe.mp4', '《红海行动》发布会《红海行动》发布会', '2018030915413794094cf209ce470fb4b2ec20d4b56d54.png', '4', '4', '1', '6', '中国', '2018-03-17', '150分钟', '2018-03-09 15:41:37');
INSERT INTO `movie` VALUES ('4', '第90届奥斯卡提名公布仪式', '20180309155433df83bf05526d4112882cc7b269a7db83.mp4', '第90届奥斯卡提名公布仪式第90届奥斯卡提名公布仪式', '201803091554338a03a2e2124f4971b7dbeef3c860065c.png', '3', '0', '0', '11', '中国', '2018-03-29', '200分钟', '2018-03-09 15:54:34');
INSERT INTO `movie` VALUES ('5', '大鱼', '20180309155809c4376a6277b044a9bd7af9b0ff77e21e.mp4', '《刺局》IP开放日独家直播', '20180309155809cb48a4eda55a4e3a984697cb003524e1.png', '3', '0', '0', '3', '中国', '2018-03-14', '120分钟', '2018-03-09 15:58:10');
INSERT INTO `movie` VALUES ('6', '《二代妖精之今生有幸》发布会', '20180309155858685dd439df2345539e39eaa069bb25fc.mp4', '《二代妖精之今生有幸》发布会', '2018030915585853409c779ee84669be20df47d72c6fc5.png', '4', '0', '0', '12', '美国', '2018-03-28', '150分钟', '2018-03-09 15:58:58');
INSERT INTO `movie` VALUES ('7', '《正义联盟》“六巨头”北京粉丝见面会', '2018030916111542eb2ea5f47f452da4a7ac4b12f58e1c.mp4', '《正义联盟》“六巨头”北京粉丝见面会《正义联盟》“六巨头”北京粉丝见面会', '20180309161115e7b1421c824d475eb5a3a7d1e7e52e97.png', '5', '9', '0', '10', '日本', '2018-03-21', '150分钟', '2018-03-09 16:11:16');
INSERT INTO `movie` VALUES ('8', '《王牌特工2：黄金圈》中国新闻发布会', '201803091614081c4d093288b54409ba41cbe9b6a3e90f.mp4', '《王牌特工2：黄金圈》中国新闻发布会《王牌特工2：黄金圈》中国新闻发布会', '201803091614084a143513f4184e0b928c23a06ccfa532.png', '4', '3', '0', '17', '俄罗斯', '2018-03-23', '130分钟', '2018-03-09 16:14:08');
INSERT INTO `movie` VALUES ('11', '《唐人街探案45》', '20180310104254ef4561604dbe4444ad7b26ede2a5d8ee.mp4', '《唐人街探案2》《唐人街探案2》', '201803101044158e07ee644e6b4ef48ac3a26ba3e05333.png', '4', '42', '1', '5', '美国', '2018-03-08', '150分钟', '2018-03-09 17:39:15');
INSERT INTO `movie` VALUES ('12', '大鱼22', '20180310114542c9fb9b7a19c14219a5f3efdd7c70ba5f.mp4', '222', '20180310114542555bade1159e413792f2fcb436be8b3b.png', '1', '1', '0', '1', '中国', '2018-03-28', '150分钟', '2018-03-10 11:45:42');
INSERT INTO `movie` VALUES ('13', '边境杀手2：边境战士', '20180310114603e84c759b51334480b6596692c16abfc8.mp4', '22', '20180310114603fecc1f99b18748daa5308f9bcac90402.png', '1', '0', '0', '1', '俄罗斯', '2018-03-15', '120分钟', '2018-03-10 11:46:04');

-- ----------------------------
-- Table structure for moviecol
-- ----------------------------
DROP TABLE IF EXISTS `moviecol`;
CREATE TABLE `moviecol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `movie_user_id` (`movie_id`,`user_id`) USING BTREE,
  KEY `user_id` (`user_id`),
  KEY `ix_moviecol_addtime` (`addtime`),
  CONSTRAINT `moviecol_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `moviecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of moviecol
-- ----------------------------
INSERT INTO `moviecol` VALUES ('2', '7', '6', '2018-03-10 14:54:19');
INSERT INTO `moviecol` VALUES ('3', '6', '4', '2018-03-10 14:54:30');
INSERT INTO `moviecol` VALUES ('4', '8', '6', '2018-03-10 14:54:40');
INSERT INTO `moviecol` VALUES ('5', '3', '1', '2018-03-10 14:54:52');
INSERT INTO `moviecol` VALUES ('7', '12', '6', '2018-03-13 15:56:41');

-- ----------------------------
-- Table structure for oplog
-- ----------------------------
DROP TABLE IF EXISTS `oplog`;
CREATE TABLE `oplog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_oplog_addtime` (`addtime`),
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of oplog
-- ----------------------------
INSERT INTO `oplog` VALUES ('1', '1', '127.0.0.1', '添加标签科幻', '2018-03-08 20:15:38');
INSERT INTO `oplog` VALUES ('2', '1', '127.0.0.1', '添加标签惊悚', '2018-03-08 20:16:08');
INSERT INTO `oplog` VALUES ('3', '1', '127.0.0.1', '添加标签-爱情', '2018-03-08 20:22:12');
INSERT INTO `oplog` VALUES ('4', '1', '127.0.0.1', '添加标签-美国', '2018-03-08 20:23:50');
INSERT INTO `oplog` VALUES ('5', '1', '127.0.0.1', '添加标签-日本', '2018-03-08 20:23:56');
INSERT INTO `oplog` VALUES ('6', '1', '127.0.0.1', '添加标签-纪录片', '2018-03-08 20:24:02');
INSERT INTO `oplog` VALUES ('7', '1', '127.0.0.1', '添加标签-喜剧', '2018-03-08 20:24:06');
INSERT INTO `oplog` VALUES ('8', '1', '127.0.0.1', '添加标签-美剧', '2018-03-08 20:24:10');
INSERT INTO `oplog` VALUES ('9', '1', '127.0.0.1', '添加标签-动画', '2018-03-08 20:24:19');
INSERT INTO `oplog` VALUES ('10', '1', '127.0.0.1', '添加标签-犯罪', '2018-03-08 20:24:24');
INSERT INTO `oplog` VALUES ('11', '1', '127.0.0.1', '添加标签-悬疑', '2018-03-08 20:24:28');
INSERT INTO `oplog` VALUES ('12', '1', '127.0.0.1', '添加标签-人性', '2018-03-08 20:24:33');
INSERT INTO `oplog` VALUES ('13', '1', '127.0.0.1', '添加标签-韩国', '2018-03-08 20:24:37');
INSERT INTO `oplog` VALUES ('14', '1', '127.0.0.1', '添加标签-英国', '2018-03-08 20:24:43');
INSERT INTO `oplog` VALUES ('15', '1', '127.0.0.1', '添加标签-青春', '2018-03-08 20:24:48');
INSERT INTO `oplog` VALUES ('16', '1', '127.0.0.1', '添加标签-温情', '2018-03-08 20:24:59');
INSERT INTO `oplog` VALUES ('17', '1', '127.0.0.1', '添加标签-动作', '2018-03-08 20:25:03');
INSERT INTO `oplog` VALUES ('18', '1', '127.0.0.1', '添加标签-奇幻', '2018-03-08 20:25:07');
INSERT INTO `oplog` VALUES ('19', '1', '127.0.0.1', '添加标签-看过的电视剧', '2018-03-08 20:25:11');
INSERT INTO `oplog` VALUES ('20', '1', '127.0.0.1', '添加标签-文艺', '2018-03-08 20:25:15');
INSERT INTO `oplog` VALUES ('21', '1', '127.0.0.1', '添加标签-家庭', '2018-03-08 20:25:20');
INSERT INTO `oplog` VALUES ('22', '1', '127.0.0.1', '添加标签-中国', '2018-03-08 20:25:23');
INSERT INTO `oplog` VALUES ('23', '1', '127.0.0.1', '添加标签-法国', '2018-03-08 20:25:31');
INSERT INTO `oplog` VALUES ('24', '1', '127.0.0.1', '添加标签-成长', '2018-03-08 20:25:36');
INSERT INTO `oplog` VALUES ('25', '1', '127.0.0.1', '添加标签-同志', '2018-03-08 20:25:42');
INSERT INTO `oplog` VALUES ('26', '1', '127.0.0.1', '添加标签-韩剧', '2018-03-08 20:25:45');
INSERT INTO `oplog` VALUES ('27', '1', '127.0.0.1', '添加标签-传记', '2018-03-08 20:25:51');
INSERT INTO `oplog` VALUES ('28', '1', '127.0.0.1', '添加标签-qqq', '2018-03-09 11:14:47');
INSERT INTO `oplog` VALUES ('29', '1', '127.0.0.1', '添加标签-qqq', '2018-03-09 11:18:31');
INSERT INTO `oplog` VALUES ('30', '1', '127.0.0.1', '添加标签-wqrwe', '2018-03-09 11:44:29');
INSERT INTO `oplog` VALUES ('31', '1', '127.0.0.1', '添加标签-卡通', '2018-03-09 15:10:16');

-- ----------------------------
-- Table structure for preview
-- ----------------------------
DROP TABLE IF EXISTS `preview`;
CREATE TABLE `preview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `logo` (`logo`),
  KEY `ix_preview_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of preview
-- ----------------------------
INSERT INTO `preview` VALUES ('1', '《唐人街探案2》', '20180310112147d098cf3e5ddd4575b0a9fb40c80a0d2d.png', '2018-03-10 11:21:47');
INSERT INTO `preview` VALUES ('2', '大鱼', '2018031011220790c8e405d2ae43f3aa4dcb2ee16659d0.png', '2018-03-10 11:22:07');
INSERT INTO `preview` VALUES ('3', '古墓丽影：源起之战', '201803101122508331afdba1874059a7f8bba1303170a2.png', '2018-03-10 11:22:51');
INSERT INTO `preview` VALUES ('4', '大坏狐狸的故事', '2018031011232034624771f1c3401bb54c9571a85dd401.jpg', '2018-03-10 11:23:21');
INSERT INTO `preview` VALUES ('5', '水形物语 ', '20180310112354618a0325a2ca4952938aeeb4eaae9306.png', '2018-03-10 11:23:54');
INSERT INTO `preview` VALUES ('6', '厉害了，我的国', '201803101124207a4e6d58cb374c23b607ec97d2ddce9b.jpg', '2018-03-10 11:24:20');
INSERT INTO `preview` VALUES ('7', '南方有乔木', '201803101124481617b479975c49f3bad4863d0c56dca9.jpg', '2018-03-10 11:24:49');
INSERT INTO `preview` VALUES ('8', '塔利 ', '201803101125069c0458fdb2704c0aa2b6f6332d600d19.jpg', '2018-03-10 11:25:07');
INSERT INTO `preview` VALUES ('9', '蚁人2：黄蜂女现身', '20180310112533effcd1cb4f594937a4f17da8c50b730b.jpg', '2018-03-10 11:25:33');
INSERT INTO `preview` VALUES ('10', '毒液：致命守护者', '201803101125455d1c3d18684949e5b31c5768aa437e65.jpg', '2018-03-10 11:25:46');
INSERT INTO `preview` VALUES ('11', 'X战警：新变种人', '20180310112559a203b8d2dea544758c8c225ae9fd5ec6.jpg', '2018-03-10 11:26:00');
INSERT INTO `preview` VALUES ('12', '钢骨', '201803101126205c199101446944ee99696a6eaeef5a86.jpg', '2018-03-10 11:26:20');
INSERT INTO `preview` VALUES ('13', '边境杀手：边境战士', '20180310114924a48f6bd99a0e4a46984aba29bc9746f1.png', '2018-03-10 11:26:55');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('1', '超级管理员', '18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,53,54', '2018-03-07 15:24:19');
INSERT INTO `role` VALUES ('2', '标签管理员', '18,19,20,21,47', '2018-03-11 13:09:28');
INSERT INTO `role` VALUES ('3', '普通管理员', '18,19,20,21,22,23,24,25,26,27,28,29,30,46,47', '2018-03-11 13:11:17');
INSERT INTO `role` VALUES ('4', '电影管理员', '18,22,23,24,47', '2018-03-11 13:11:35');
INSERT INTO `role` VALUES ('5', '会员管理员', '25,26,27,47', '2018-03-11 13:11:50');
INSERT INTO `role` VALUES ('6', '查看管理员', '18,20,23,26,29,32,38,41,44,46,47', '2018-03-11 13:12:10');
INSERT INTO `role` VALUES ('7', '编辑管理员', '18,19,20,22,23,25,26,28,29,31,32,34,35,46,47', '2018-03-11 13:12:28');

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tag_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES ('1', '科幻', '2018-03-08 20:15:38');
INSERT INTO `tag` VALUES ('2', '惊悚', '2018-03-08 20:16:08');
INSERT INTO `tag` VALUES ('3', '爱情', '2018-03-08 20:22:12');
INSERT INTO `tag` VALUES ('4', '美国', '2018-03-08 20:23:50');
INSERT INTO `tag` VALUES ('5', '日本', '2018-03-08 20:23:56');
INSERT INTO `tag` VALUES ('6', '纪录片', '2018-03-08 20:24:01');
INSERT INTO `tag` VALUES ('7', '喜剧', '2018-03-08 20:24:06');
INSERT INTO `tag` VALUES ('8', '美剧', '2018-03-08 20:24:10');
INSERT INTO `tag` VALUES ('9', '动画', '2018-03-08 20:24:19');
INSERT INTO `tag` VALUES ('10', '犯罪', '2018-03-08 20:24:24');
INSERT INTO `tag` VALUES ('11', '悬疑', '2018-03-08 20:24:28');
INSERT INTO `tag` VALUES ('12', '人性', '2018-03-08 20:24:33');
INSERT INTO `tag` VALUES ('13', '韩国', '2018-03-08 20:24:37');
INSERT INTO `tag` VALUES ('14', '英国', '2018-03-08 20:24:42');
INSERT INTO `tag` VALUES ('15', '青春', '2018-03-08 20:24:48');
INSERT INTO `tag` VALUES ('16', '温情', '2018-03-08 20:24:58');
INSERT INTO `tag` VALUES ('17', '动作', '2018-03-08 20:25:03');
INSERT INTO `tag` VALUES ('18', '奇幻', '2018-03-08 20:25:07');
INSERT INTO `tag` VALUES ('19', '看过电视剧', '2018-03-08 20:25:11');
INSERT INTO `tag` VALUES ('20', '文艺', '2018-03-08 20:25:15');
INSERT INTO `tag` VALUES ('21', '家庭', '2018-03-08 20:25:19');
INSERT INTO `tag` VALUES ('22', '中国', '2018-03-08 20:25:23');
INSERT INTO `tag` VALUES ('23', '法国', '2018-03-08 20:25:31');
INSERT INTO `tag` VALUES ('24', '成长', '2018-03-08 20:25:36');
INSERT INTO `tag` VALUES ('25', '同志', '2018-03-08 20:25:42');
INSERT INTO `tag` VALUES ('26', '韩剧', '2018-03-08 20:25:45');
INSERT INTO `tag` VALUES ('27', '传记', '2018-03-08 20:25:50');
INSERT INTO `tag` VALUES ('31', '卡通', '2018-03-09 15:10:16');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `info` text,
  `face` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `face` (`face`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_user_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', '张三', 'jHH2BKvDpWX8MRMpn4qGBr13Vr2875fY', '747097006@qq.com', '18565695464', '牛逼', '20180310114924a48f6bd99a0e4a46984aba29bc9746f1.png', '2018-03-10 12:28:51', '1520656183');
INSERT INTO `user` VALUES ('4', '李四', 'jHH2BKvDpWX8MRMpn4qGBr13Vr2875fY', '7470937006@qq.com', '18565795464', '呵呵', '20180310114924a48f6bd99a0e4a46984aba29bc96746f1.png', '2018-03-10 14:07:29', '15203656183');
INSERT INTO `user` VALUES ('5', '王五', 'jHH2BKvDpW3X8MRMpn4qGBr13Vr2875fY', '7570937006@qq.com', '18565995464', '哈哈', '20180310114924a48f68d99a0e4a46984aba29bc96746f1.png', '2018-03-10 14:08:59', '152034656183');
INSERT INTO `user` VALUES ('6', '张三三', 'pbkdf2:sha256:50000$kW0Xjc1b$8f65afce803a71da17c41974fc67e70603ee41e15c223990a90b12dd5a0e186c', '7471097040@qq.com', '18565935464', '土地是以它的肥沃和收获而被估价的；才能也是土地，不过它生产的不是粮食，而是真理。如果只能滋生瞑想和幻想的话，即使再大的才能也只是砂地或盐池，那上面连小草也长不出来的。', '201803121526135d03b1fec8ed45a4b5675e4138411cde.png', '2018-03-12 11:39:25', '41feecac3bc241ae83b2ef8e66a8b920');

-- ----------------------------
-- Table structure for userlog
-- ----------------------------
DROP TABLE IF EXISTS `userlog`;
CREATE TABLE `userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_userlog_addtime` (`addtime`),
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userlog
-- ----------------------------
INSERT INTO `userlog` VALUES ('1', '1', '127.0.0.1', '2018-03-10 16:39:55');
INSERT INTO `userlog` VALUES ('2', '4', '127.0.0.1', '2018-03-10 16:40:11');
INSERT INTO `userlog` VALUES ('3', '5', '127.0.0.1', '2018-03-10 16:40:33');
INSERT INTO `userlog` VALUES ('4', '4', '192.168.4.9', '2018-03-10 16:40:47');
INSERT INTO `userlog` VALUES ('5', '6', '127.0.0.1', '2018-03-12 12:00:33');
INSERT INTO `userlog` VALUES ('6', '6', '127.0.0.1', '2018-03-12 12:03:35');
INSERT INTO `userlog` VALUES ('7', '6', '127.0.0.1', '2018-03-12 12:04:30');
INSERT INTO `userlog` VALUES ('8', '6', '127.0.0.1', '2018-03-12 12:05:30');
INSERT INTO `userlog` VALUES ('9', '6', '127.0.0.1', '2018-03-12 12:06:27');
INSERT INTO `userlog` VALUES ('10', '6', '127.0.0.1', '2018-03-12 14:09:42');
INSERT INTO `userlog` VALUES ('11', '6', '127.0.0.1', '2018-03-12 15:13:47');
INSERT INTO `userlog` VALUES ('12', '6', '127.0.0.1', '2018-03-12 15:48:30');
INSERT INTO `userlog` VALUES ('13', '6', '127.0.0.1', '2018-03-12 15:51:04');
INSERT INTO `userlog` VALUES ('14', '6', '127.0.0.1', '2018-03-13 14:55:06');
INSERT INTO `userlog` VALUES ('15', '6', '127.0.0.1', '2018-03-13 15:06:04');
