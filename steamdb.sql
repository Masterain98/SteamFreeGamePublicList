-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1
-- 生成日期： 2020-05-28 13:07:43
-- 服务器版本： 10.4.12-MariaDB-log
-- PHP 版本： 7.2.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `steamdb`
--

-- --------------------------------------------------------

--
-- 表的结构 `asf`
--

CREATE TABLE `asf` (
  `display` int(11) NOT NULL,
  `command` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `asf`
--

INSERT INTO `asf` (`display`, `command`) VALUES
(1, 'addlicense ASF sub/454706, sub/454711, sub/454715, sub/456209, sub/456210, sub/459452, sub/461588, sub/465037, sub/462714');

-- --------------------------------------------------------

--
-- 表的结构 `freeGame`
--

CREATE TABLE `freeGame` (
  `game_name` text NOT NULL,
  `sub_id` text NOT NULL,
  `steam_link` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `freeGame`
--

INSERT INTO `freeGame` (`game_name`, `sub_id`, `steam_link`) VALUES
('Tennis World Tour - DLC 11 - Garcia', '454706', 'https://store.steampowered.com/app/640590/?curator_clanid=4777282&utm_source=SteamDB'),
('Tennis World Tour - DLC 14 - Shapovalov', '454711', 'https://store.steampowered.com/app/640590/?curator_clanid=4777282&utm_source=SteamDB'),
('Tennis World Tour - DLC 13 - De Minaur', '454715', 'https://store.steampowered.com/app/640590/?curator_clanid=4777282&utm_source=SteamDB'),
('Tennis World Tour - DLC 14 - Shapovalov', '456209', 'https://store.steampowered.com/app/640590/?curator_clanid=4777282&utm_source=SteamDB'),
('Tennis World Tour - DLC 11 - Garcia', '456210', 'https://store.steampowered.com/app/640590/?curator_clanid=4777282&utm_source=SteamDB'),
('Showdown Bandit', '459452', 'https://store.steampowered.com/app/640590/?curator_clanid=4777282&utm_source=SteamDB'),
('10 Second Ninja X', '461588', 'https://store.steampowered.com/app/371140/?curator_clanid=4777282&utm_source=SteamDB'),
('Interkosmos', '465037', 'https://store.steampowered.com/app/371140/?curator_clanid=4777282&utm_source=SteamDB'),
('Aegis Defenders', '462714', 'https://store.steampowered.com/app/371140/?curator_clanid=4777282&utm_source=SteamDB');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
