-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-03-2026 a las 15:45:37
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `cositop`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

CREATE TABLE `estudiantes` (
  `Id_estudiante` int(11) NOT NULL,
  `Nombre_estudiante` varchar(50) NOT NULL,
  `Edad_estudiante` int(11) NOT NULL,
  `Carrera_estudiante` varchar(50) NOT NULL,
  `Nota1` decimal(10,0) DEFAULT NULL,
  `Nota2` decimal(10,0) DEFAULT NULL,
  `Nota3` decimal(10,0) DEFAULT NULL,
  `Promedio` decimal(10,0) DEFAULT NULL,
  `Desempeño` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`Id_estudiante`, `Nombre_estudiante`, `Edad_estudiante`, `Carrera_estudiante`, `Nota1`, `Nota2`, `Nota3`, `Promedio`, `Desempeño`) VALUES
(1, 'Ana', 18, 'Ingenieria', 2, 5, 3, 3, 'Regular'),
(2, 'Maria', 23, 'Ingenieria', 5, 4, 3, 4, 'Bueno'),
(3, 'Luis', 22, 'Matematicas', 2, 3, 4, 3, 'Regular'),
(4, 'Ana', 21, 'Ingenieria', 5, 5, 5, 5, 'Excelente'),
(5, 'Maria', 23, 'Ingenieria', 4, 3, 3, 3, 'Regular'),
(6, 'Ana', 20, 'Fisica', 2, 3, 3, 2, 'Regular'),
(7, 'Luis', 20, 'Ingenieria', 4, 2, 4, 3, 'Bueno'),
(8, 'Luis', 23, 'Fisica', 4, 3, 2, 3, 'Regular'),
(9, 'Luis', 22, 'Ingenieria', 3, 3, 2, 2, 'Regular'),
(10, 'Ana', 20, 'Fisica', 5, 3, 2, 3, 'Regular'),
(11, 'Carlos', 19, 'Fisica', 4, 2, 2, 2, 'Regular'),
(12, 'Luis', 21, 'Fisica', 2, 5, 5, 4, 'Bueno'),
(13, 'Maria', 22, 'Fisica', 5, 2, 2, 3, 'Regular'),
(14, 'Jose', 18, 'Fisica', 4, 3, 2, 3, 'Regular'),
(15, 'Paula', 21, 'Fisica', 5, 4, 2, 3, 'Bueno'),
(16, 'Luis', 22, 'Ingenieria', 2, 3, 2, 2, 'Deficiente'),
(17, 'Maria', 22, 'Matematicas', 5, 5, 2, 4, 'Bueno'),
(18, 'Luis', 20, 'Matematicas', 5, 4, 5, 4, 'Excelente'),
(19, 'Ana', 22, 'Ingenieria', 2, 3, 4, 3, 'Regular'),
(20, 'Ana', 20, 'Fisica', 3, 5, 2, 3, 'Bueno'),
(21, 'Carlos', 20, 'Ingenieria', 2, 4, 5, 3, 'Bueno'),
(22, 'Luis', 23, 'Fisica', 3, 2, 5, 3, 'Bueno'),
(23, 'Ana', 21, 'Ingenieria', 3, 5, 4, 4, 'Bueno'),
(24, 'Carlos', 19, 'Matematicas', 4, 3, 3, 3, 'Regular'),
(25, 'Maria', 18, 'Fisica', 3, 3, 5, 3, 'Bueno'),
(26, 'Carlos', 22, 'Matematicas', 3, 4, 2, 3, 'Regular'),
(27, 'Luis', 21, 'Ingenieria', 2, 3, 5, 3, 'Regular'),
(28, 'Jose', 20, 'Matematicas', 4, 3, 3, 3, 'Regular'),
(29, 'Ana', 19, 'Ingenieria', 3, 2, 3, 3, 'Regular'),
(30, 'Maria', 18, 'Ingenieria', 5, 4, 4, 4, 'Excelente'),
(31, 'Maria', 23, 'Fisica', 2, 3, 4, 3, 'Regular'),
(32, 'Jose', 18, 'Matematicas', 5, 3, 4, 4, 'Bueno'),
(33, 'Ana', 18, 'Matematicas', 5, 2, 5, 4, 'Bueno'),
(34, 'Jose', 20, 'Fisica', 2, 2, 2, 2, 'Deficiente'),
(35, 'Paula', 23, 'Fisica', 5, 5, 3, 4, 'Bueno'),
(36, 'Jose', 18, 'Fisica', 4, 3, 3, 3, 'Bueno'),
(37, 'Ana', 21, 'Fisica', 5, 3, 5, 4, 'Excelente'),
(38, 'Ana', 22, 'Ingenieria', 3, 5, 2, 3, 'Bueno'),
(39, 'Ana', 23, 'Fisica', 3, 2, 2, 2, 'Regular'),
(40, 'Luis', 18, 'Fisica', 3, 3, 4, 3, 'Bueno'),
(41, 'Luis', 23, 'Fisica', 3, 4, 3, 3, 'Bueno'),
(42, 'Ana', 22, 'Fisica', 2, 5, 3, 3, 'Regular'),
(43, 'Maria', 21, 'Fisica', 5, 5, 4, 4, 'Excelente'),
(44, 'Paula', 20, 'Matematicas', 2, 3, 2, 2, 'Deficiente'),
(45, 'Ana', 18, 'Fisica', 5, 2, 2, 3, 'Regular'),
(46, 'Maria Lopez', 35, 'Administracion Empresas', 4, 1, 3, 3, 'Bajo'),
(47, 'Valentina Mora', 28, 'Derecho', 1, 1, 3, 2, 'Bajo'),
(48, 'Andres Torres', 27, 'Derecho', 5, 1, 5, 4, 'Regular'),
(49, 'Valentina Mora', 24, 'Contaduria', 3, 3, 1, 3, 'Bajo'),
(50, 'Juan Perez', 24, 'Psicologia', 0, 3, 1, 1, 'Bajo'),
(51, 'Andres Torres', 30, 'Arquitectura', 0, 4, 2, 2, 'Bajo'),
(52, 'Sofia Herrera', 22, 'Medicina', 3, 1, 3, 3, 'Bajo'),
(53, 'Felipe Vargas', 23, 'Arquitectura', 1, 4, 0, 2, 'Bajo'),
(54, 'Felipe Vargas', 15, 'Administracion Empresas', 3, 1, 2, 2, 'Bajo'),
(55, 'Daniela Cruz', 13, 'Derecho', 1, 1, 4, 2, 'Bajo'),
(56, 'Jose Castro', 17, 'Medicina', 5, 1, 4, 3, 'Regular'),
(57, 'Ana Rodriguez', 17, 'Ingenieria Sistemas', 4, 3, 4, 4, 'Regular'),
(58, 'Laura Gutierrez', 21, 'Ingenieria Industrial', 2, 2, 1, 2, 'Bajo'),
(59, 'Daniela Cruz', 25, 'Administracion Empresas', 4, 5, 3, 4, 'Bueno'),
(60, 'Felipe Vargas', 27, 'Contaduria', 1, 3, 5, 3, 'Regular'),
(61, 'Valentina Mora', 0, 'Ingenieria Industrial', 4, 3, 5, 4, 'Bueno'),
(62, 'Maria Lopez', 17, 'Ingenieria Industrial', 4, 0, 2, 2, 'Bajo'),
(63, 'Luis Martinez', 15, 'Arquitectura', 1, 1, 3, 2, 'Bajo'),
(64, 'Laura Gutierrez', 24, 'Ingenieria Sistemas', 2, 3, 3, 3, 'Bajo'),
(65, 'Laura Gutierrez', 6, 'Psicologia', 4, 3, 0, 2, 'Bajo'),
(66, 'Sebastian Ruiz', 29, 'Ingenieria Industrial', 5, 2, 2, 3, 'Bajo'),
(67, 'Maria Lopez', 35, 'Administracion Empresas', 4, 1, 3, 3, 'Bajo'),
(68, 'Valentina Mora', 28, 'Derecho', 1, 1, 3, 2, 'Bajo'),
(69, 'Andres Torres', 27, 'Derecho', 5, 1, 5, 4, 'Regular'),
(70, 'Valentina Mora', 24, 'Contaduria', 3, 3, 1, 3, 'Bajo'),
(71, 'Juan Perez', 24, 'Psicologia', 0, 3, 1, 1, 'Bajo'),
(72, 'Andres Torres', 30, 'Arquitectura', 0, 4, 2, 2, 'Bajo'),
(73, 'Sofia Herrera', 22, 'Medicina', 3, 1, 3, 3, 'Bajo'),
(74, 'Felipe Vargas', 23, 'Arquitectura', 1, 4, 0, 2, 'Bajo'),
(75, 'Felipe Vargas', 15, 'Administracion Empresas', 3, 1, 2, 2, 'Bajo'),
(76, 'Daniela Cruz', 13, 'Derecho', 1, 1, 4, 2, 'Bajo'),
(77, 'Jose Castro', 17, 'Medicina', 5, 1, 4, 3, 'Regular'),
(78, 'Ana Rodriguez', 17, 'Ingenieria Sistemas', 4, 3, 4, 4, 'Regular'),
(79, 'Laura Gutierrez', 21, 'Ingenieria Industrial', 2, 2, 1, 2, 'Bajo'),
(80, 'Daniela Cruz', 25, 'Administracion Empresas', 4, 5, 3, 4, 'Bueno'),
(81, 'Felipe Vargas', 27, 'Contaduria', 1, 3, 5, 3, 'Regular'),
(82, 'Valentina Mora', 0, 'Ingenieria Industrial', 4, 3, 5, 4, 'Bueno'),
(83, 'Maria Lopez', 17, 'Ingenieria Industrial', 4, 0, 2, 2, 'Bajo'),
(84, 'Luis Martinez', 15, 'Arquitectura', 1, 1, 3, 2, 'Bajo'),
(85, 'Laura Gutierrez', 24, 'Ingenieria Sistemas', 2, 3, 3, 3, 'Bajo'),
(86, 'Laura Gutierrez', 6, 'Psicologia', 4, 3, 0, 2, 'Bajo'),
(87, 'Sebastian Ruiz', 29, 'Ingenieria Industrial', 5, 2, 2, 3, 'Bajo'),
(88, 'Maria Lopez', 35, 'Administracion Empresas', 4, 1, 3, 3, 'Bajo'),
(89, 'Valentina Mora', 28, 'Derecho', 1, 1, 3, 2, 'Bajo'),
(90, 'Andres Torres', 27, 'Derecho', 5, 1, 5, 4, 'Regular'),
(91, 'Valentina Mora', 24, 'Contaduria', 3, 3, 1, 3, 'Bajo'),
(92, 'Juan Perez', 24, 'Psicologia', 0, 3, 1, 1, 'Bajo'),
(93, 'Andres Torres', 30, 'Arquitectura', 0, 4, 2, 2, 'Bajo'),
(94, 'Sofia Herrera', 22, 'Medicina', 3, 1, 3, 3, 'Bajo'),
(95, 'Felipe Vargas', 23, 'Arquitectura', 1, 4, 0, 2, 'Bajo'),
(96, 'Felipe Vargas', 15, 'Administracion Empresas', 3, 1, 2, 2, 'Bajo'),
(97, 'Daniela Cruz', 13, 'Derecho', 1, 1, 4, 2, 'Bajo'),
(98, 'Jose Castro', 17, 'Medicina', 5, 1, 4, 3, 'Regular'),
(99, 'Ana Rodriguez', 17, 'Ingenieria Sistemas', 4, 3, 4, 4, 'Regular'),
(100, 'Laura Gutierrez', 21, 'Ingenieria Industrial', 2, 2, 1, 2, 'Bajo'),
(101, 'Daniela Cruz', 25, 'Administracion Empresas', 4, 5, 3, 4, 'Bueno'),
(102, 'Felipe Vargas', 27, 'Contaduria', 1, 3, 5, 3, 'Regular'),
(103, 'Valentina Mora', 0, 'Ingenieria Industrial', 4, 3, 5, 4, 'Bueno'),
(104, 'Maria Lopez', 17, 'Ingenieria Industrial', 4, 0, 2, 2, 'Bajo'),
(105, 'Luis Martinez', 15, 'Arquitectura', 1, 1, 3, 2, 'Bajo'),
(106, 'Laura Gutierrez', 24, 'Ingenieria Sistemas', 2, 3, 3, 3, 'Bajo'),
(107, 'Laura Gutierrez', 6, 'Psicologia', 4, 3, 0, 2, 'Bajo'),
(108, 'Sebastian Ruiz', 29, 'Ingenieria Industrial', 5, 2, 2, 3, 'Bajo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `Id_usuario` int(11) NOT NULL,
  `Username` varchar(40) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Rolusuario` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`Id_usuario`, `Username`, `Password`, `Rolusuario`) VALUES
(1, 'pedro', '123', 'admin'),
(2, 'juan', '123', 'profesor');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`Id_estudiante`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`Id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `Id_estudiante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=109;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `Id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
