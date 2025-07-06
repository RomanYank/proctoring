-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Июл 06 2025 г., 20:09
-- Версия сервера: 8.0.30
-- Версия PHP: 8.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `project_db`
--

-- --------------------------------------------------------

--
-- Структура таблицы `department`
--

CREATE TABLE `department` (
  `id` int NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `recording_time` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `department`
--

INSERT INTO `department` (`id`, `name`, `recording_time`) VALUES
(1, 'Тестовая организация', 10),
(2, 'Тестовая организация', 200000000),
(3, 'Создание новой организации', 30),
(4, 'ООО Тестик', 11111);

-- --------------------------------------------------------

--
-- Структура таблицы `queue`
--

CREATE TABLE `queue` (
  `id` int NOT NULL,
  `channel` varchar(255) NOT NULL,
  `job` blob NOT NULL,
  `pushed_at` int NOT NULL,
  `ttr` int NOT NULL,
  `delay` int NOT NULL DEFAULT '0',
  `priority` int UNSIGNED NOT NULL DEFAULT '1024',
  `reserved_at` int DEFAULT NULL,
  `attempt` int DEFAULT NULL,
  `done_at` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `queue`
--

INSERT INTO `queue` (`id`, `channel`, `job`, `pushed_at`, `ttr`, `delay`, `priority`, `reserved_at`, `attempt`, `done_at`) VALUES
(35, 'default', 0x4f3a32323a22636f6d6d6f6e5c6a6f62735c416e616c797a654a6f62223a323a7b733a393a22766964656f50617468223b733a3130343a22433a5c4f5350616e656c5c646f6d61696e735c70726f6a6563742e6c6f63616c686f73745c7075626c69632f66726f6e74656e642f7765622f7265636f72642f766964656f2f57656243616d6572612d323032353531372d63667a7368786c337862362e7765626d223b733a373a22766964656f4964223b693a34333b7d, 1750179358, 300, 0, 1024, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `user`
--

CREATE TABLE `user` (
  `id` int NOT NULL,
  `username` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` int NOT NULL,
  `auth_key` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` int NOT NULL,
  `department_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `user`
--

INSERT INTO `user` (`id`, `username`, `full_name`, `password`, `status`, `auth_key`, `role`, `department_id`) VALUES
(1, 'root', '', '63a9f0ea7bb98050796b649e85481845', 10, 'auth-1', 1, 1),
(2, 'user3', 'Тестовый Тест Тестович', 'ee11cbb19052e40b07aac0ca060c23ee', 10, 'auth-2', 0, 2),
(3, 'user2', 'Янковский Роман Денисович', '7e58d63b60197ceb55a1c487989a3720', 10, 'auth-3', 0, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `video_files`
--

CREATE TABLE `video_files` (
  `id` int NOT NULL,
  `web_camera_video` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `capture_screen_video` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `user_id` int NOT NULL,
  `violations` json DEFAULT NULL,
  `verify` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `video_files`
--

INSERT INTO `video_files` (`id`, `web_camera_video`, `capture_screen_video`, `date`, `user_id`, `violations`, `verify`) VALUES
(41, 'WebCamera-202552-afus8lu1byn.webm', 'CaptureScreen-202552-eaw850yi5xl.webm', '2025-06-02', 3, '\"[{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:02\\\",\\\"violation\\\":\\\"Отклонение головы (right)\\\"},{\\\"time\\\":\\\"00:03\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:03\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:04\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:05\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:05\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:05\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:05\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:05\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:05\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:05\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:05\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:07\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:07\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:07\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:07\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:07\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:07\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:07\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:08\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:09\\\",\\\"violation\\\":\\\"Использование телефона\\\"}]\"', 1),
(42, 'WebCamera-202552-m4r9tlgo0s6.webm', 'CaptureScreen-202552-lqb4oy5bo4.webm', '2025-06-02', 3, '\"[{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Отклонение головы (left)\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:00\\\",\\\"violation\\\":\\\"Использование телефона\\\"},{\\\"time\\\":\\\"00:01\\\",\\\"violation\\\":\\\"Использование телефона\\\"}]\"', 1),
(43, 'WebCamera-2025517-cfzshxl3xb6.webm', 'CaptureScreen-2025517-begw47q058.webm', '2025-06-17', 3, NULL, 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `queue`
--
ALTER TABLE `queue`
  ADD PRIMARY KEY (`id`),
  ADD KEY `channel` (`channel`),
  ADD KEY `reserved_at` (`reserved_at`),
  ADD KEY `priority` (`priority`);

--
-- Индексы таблицы `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_ibfk_1` (`department_id`);

--
-- Индексы таблицы `video_files`
--
ALTER TABLE `video_files`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `department`
--
ALTER TABLE `department`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `queue`
--
ALTER TABLE `queue`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT для таблицы `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `video_files`
--
ALTER TABLE `video_files`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`);

--
-- Ограничения внешнего ключа таблицы `video_files`
--
ALTER TABLE `video_files`
  ADD CONSTRAINT `video_files_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
